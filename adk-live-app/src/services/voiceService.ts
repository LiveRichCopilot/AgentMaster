import type { VoiceSettings } from '../types';

class VoiceService {
  private recognition: any = null;
  private synthesis: SpeechSynthesis;
  private isListening: boolean = false;
  private voices: SpeechSynthesisVoice[] = [];
  private settings: VoiceSettings = {
    enabled: true,
    pitch: 1.0,
    rate: 1.0,
    volume: 1.0,
  };

  constructor() {
    this.synthesis = window.speechSynthesis;

    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = true;
      this.recognition.lang = 'en-US';
    }

    this.loadVoices();
    if (this.synthesis.onvoiceschanged !== undefined) {
      this.synthesis.onvoiceschanged = () => this.loadVoices();
    }
  }

  private loadVoices() {
    this.voices = this.synthesis.getVoices();
    const femaleVoice = this.voices.find(
      voice => voice.name.toLowerCase().includes('female') ||
               voice.name.toLowerCase().includes('samantha') ||
               voice.name.toLowerCase().includes('karen') ||
               voice.name.toLowerCase().includes('victoria')
    );
    if (femaleVoice) {
      this.settings.voice = femaleVoice.name;
    }
  }

  startListening(
    onResult: (transcript: string, isFinal: boolean) => void,
    onEnd?: () => void,
    onError?: (error: any) => void
  ) {
    if (!this.recognition) {
      onError?.(new Error('Speech recognition not supported'));
      return;
    }

    if (this.isListening) {
      return;
    }

    this.isListening = true;

    this.recognition.onresult = (event: any) => {
      const result = event.results[event.results.length - 1];
      const transcript = result[0].transcript;
      onResult(transcript, result.isFinal);
    };

    this.recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error);
      this.isListening = false;
      onError?.(event.error);
    };

    this.recognition.onend = () => {
      this.isListening = false;
      onEnd?.();
    };

    this.recognition.start();
  }

  stopListening() {
    if (this.recognition && this.isListening) {
      this.recognition.stop();
      this.isListening = false;
    }
  }

  speak(text: string, onEnd?: () => void) {
    if (!this.settings.enabled) {
      onEnd?.();
      return;
    }

    this.synthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.pitch = this.settings.pitch;
    utterance.rate = this.settings.rate;
    utterance.volume = this.settings.volume;

    if (this.settings.voice) {
      const voice = this.voices.find(v => v.name === this.settings.voice);
      if (voice) {
        utterance.voice = voice;
      }
    }

    utterance.onend = () => {
      onEnd?.();
    };

    this.synthesis.speak(utterance);
  }

  stopSpeaking() {
    this.synthesis.cancel();
  }

  updateSettings(settings: Partial<VoiceSettings>) {
    this.settings = { ...this.settings, ...settings };
  }

  getSettings(): VoiceSettings {
    return { ...this.settings };
  }

  isRecognitionAvailable(): boolean {
    return this.recognition !== null;
  }

  isSpeaking(): boolean {
    return this.synthesis.speaking;
  }

  getVoices(): SpeechSynthesisVoice[] {
    return this.voices;
  }
}

export const voiceService = new VoiceService();
