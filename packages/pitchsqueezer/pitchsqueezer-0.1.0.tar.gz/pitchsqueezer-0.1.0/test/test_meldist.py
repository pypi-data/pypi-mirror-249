import pitch_squeezer as ps
import sys
#sys.path.append("../src")
#import pitch_squeezer_bak as ps
#import pitch_squeezer_fast as ps
import librosa
import pyworld as pw
import numpy as np
import time
import matplotlib.pyplot as plt
import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.basic_tools as basic
import parselmouth
import soundfile as sf
import os

def get_errors(test_f0, ref_f0):
    
    plt.plot(test_f0,"blue")
    plt.plot(ref_f0, "black")
    gross_frames = np.zeros(len(test_f0))
  
    for i in range(len(test_f0)):
        if test_f0[i] > 0 and ref_f0[i] > 0 and np.abs(test_f0[i]-ref_f0[i]) > 0.2*ref_f0[i]:
            gross_frames[i] = test_f0[i]
    plt.plot(gross_frames, "red", linewidth=2)
    plt.show()
  
    voicing_errors = np.logical_xor(ref_f0 == 0, test_f0 == 0)
    voicing_errors = np.sum(voicing_errors)/len(ref_f0)*100
    voiced_frames = np.logical_and(ref_f0 > 0, test_f0 > 0)
    test_f0 = test_f0[voiced_frames]
    ref_f0 = ref_f0[voiced_frames]
    errors = np.abs(test_f0 - ref_f0)
    gross_errors = errors > 0.2 * ref_f0
    percentage_gross_errors = (np.sum(gross_errors) / len(errors)) * 100
    fine_errors = errors[~gross_errors]
    mean_fine_errors = np.mean(fine_errors)
    
  
    return voicing_errors, percentage_gross_errors, mean_fine_errors


def analysis(wav, fmin, fmax, method = "squeezer"):
    
    if method == "squeezer":
        f0_ps, if0_ps = ps.track_pitch(wav, min_hz=fmin, max_hz=fmax, voicing_thresh=0.45,frame_rate=100, viterbi=False)
        #f0_ps = f0_ps[1:]
       
        return f0_ps
    
    elif method == "yaapt":
        signal = basic.SignalObj(wav)
        f0_pyaapt = pYAAPT.yaapt(signal, **{'f0_min' : fmin, 'f0_max':fmax, 'frame_space' : 10.0})
        f0_pyaapt = f0_pyaapt.samp_values
        f0_pyaapt = np.pad(f0_pyaapt, 1, 'edge')
        return f0_pyaapt
   
    elif method == "pyin":
        x, fs = librosa.load(wav, sr=None)
       
        f0_pyin, voiced_flag, voiced_probs = librosa.pyin(x,sr=fs, fmin=fmin, fmax=fmax, hop_length = int(fs/100))
        f0_pyin[np.isnan(f0_pyin)]=0
        f0_pyin = f0_pyin[1:]
        np.insert(f0_pyin,1,0)
        return f0_pyin

    elif method == "praat":
        sound = parselmouth.Sound(wav)
        pitch = sound.to_pitch_ac(time_step = 0.01, pitch_floor=fmin, pitch_ceiling=fmax)
        pitch = pitch.selected_array['frequency']
        pitch = np.pad(pitch, 2, 'edge')
        return pitch
    
    elif  method == "swipe":
        import libf0
        x, fs = librosa.load(wav, sr=None)
       
        return f0_swipe
    
    else:
        print(method+" not implemented")
        return None
    
def synthesis(wav, f0):
    x, fs, = librosa.load(wav, sr=16000)
    x = np.array(x, dtype=np.double)
    _f0, t = pw.dio(x, fs,frame_period=10)    # raw pitch extractor
    
    #f0 = pw.stonemask(x, _f0, t, fs)  # pitch refinement
 
    #f0 = f0[:len(_f0)]
    ap = pw.d4c(x, f0, t, fs)         # extract aperiodicity
    ap[:] = 0.
    sp = pw.cheaptrick(x, f0, t, fs)
    y1 = pw.synthesize(f0, sp, ap, fs, frame_period=10)
    sf.write("output.wav", y1, fs)
    #os.system("afplay output.wav -t 10 &")
    return y1

    
if __name__ == "__main__":
    import sys, glob, time
    import librosa
    import pyworld as pw
    test_files = sorted(glob.glob(sys.argv[1]+"/*/signal.wav"))
    ref_files = sorted(glob.glob(sys.argv[1]+"/*/*.npy"))

    for f, r in zip(test_files, ref_files):
    
    
        #print("evaluating "+method,end=": ", flush=True)
        start = time.time()
        refs = []
        tests = []
        y, sr = librosa.load(f,sr=16000)
        y = (y-np.mean(y))/np.std(y)
        orig_mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=300,win_length=int(sr/8),hop_length=int(sr/100))
        #plt.imshow(np.log(orig_mel+0.001), aspect="auto",origin="lower",cmap="inferno")
        #plt.show()

        ref = np.load(r)
        ref_f0 = np.array([item[1] for item in ref])
        if r.find("/m") > 0:
            ref_f0[ref_f0<70]=0
        if r.find("/f") > 0:
            ref_f0[ref_f0<110]=0
      
        print("analyzing "+f)
        for method in ("ref", "squeezer", "swipe",): # "swipe", "praat", "yaapt", "pyin"):
        
           
            if method == "ref":
                f0 = ref_f0
            else:
                f0 = analysis(f, 50, 500, method)
            #f0 = np.pad(f0, (0,10))
            #f0 = f0[:orig_mel.shape[1]-1]
            
            y2= synthesis(f, f0)
            #print(len(y2), len(y))
            y2 = (y2-np.mean(y2))/np.std(y2)
            test_mel = librosa.feature.melspectrogram(y=y2, sr=sr, n_mels=300,win_length=int(sr/8),hop_length = int(sr/100))
            test_mel = test_mel[:,:orig_mel.shape[1]]
            print(test_mel.shape, orig_mel.shape)
            rmse = np.mean(np.abs(orig_mel-test_mel))
            print(method, rmse)
            #plt.figure()
            #plt.imshow(np.log(test_mel+0.001), aspect="auto",origin="lower",cmap="inferno")
            #plt.show()
            # match lengths (for all methods, 1 frame off only)
            # print(len(f0[f0>0]), len(ref_f0[ref_f0>0]))
            f0 = f0[:len(ref_f0)]
            ref_f0 = ref_f0[:len(f0)]
            print(r, get_errors(f0, ref_f0))
            #plt.plot(f0, label=method)
            #plt.legend()
            #plt.show()
            refs.append(ref_f0)
            tests.append(f0)
        """
        ref_f0= np.concatenate(refs, axis=None)
        test_f0= np.concatenate(tests, axis=None)
        print("\nnum voiced frames, test:",len(test_f0[test_f0>0]), "ref:",len(ref_f0[ref_f0>0]))
        vde, gpe, fpe = get_errors(test_f0, ref_f0)
        print(" done in ", time.time()-start, "seconds")
        print("vde " +str(vde)+"% gpe "+str(gpe)+"% fpe "+str(fpe)+"hz\n")
        """
   
