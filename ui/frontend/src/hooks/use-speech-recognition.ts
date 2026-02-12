"use client";

import { useState, useEffect, useCallback } from "react";

interface UseSpeechRecognitionReturn {
    isListening: boolean;
    transcript: string;
    startListening: () => void;
    stopListening: () => void;
    isSupported: boolean;
}

export function useSpeechRecognition(): UseSpeechRecognitionReturn {
    const [isListening, setIsListening] = useState(false);
    const [transcript, setTranscript] = useState("");
    const [isSupported, setIsSupported] = useState(false);
    const [recognitionInstance, setRecognitionInstance] = useState<any>(null);

    useEffect(() => {
        // Check if browser supports Speech Recognition
        if (typeof window !== "undefined") {
            const SpeechRecognition =
                (window as any).SpeechRecognition ||
                (window as any).webkitSpeechRecognition;

            if (SpeechRecognition) {
                setIsSupported(true);
                const newRecognition = new SpeechRecognition();
                newRecognition.continuous = false;
                newRecognition.interimResults = true;
                newRecognition.lang = "en-US";

                newRecognition.onresult = (event: any) => {
                    const results = event.results;
                    const finalTranscript = Array.from(results)
                        .map((result: any) => result[0].transcript)
                        .join("");
                    setTranscript(finalTranscript);
                };

                newRecognition.onend = () => {
                    setIsListening(false);
                };

                newRecognition.onerror = (event: any) => {
                    console.error("Speech recognition error:", event.error);
                    setIsListening(false);
                };

                setRecognitionInstance(newRecognition);
            }
        }
    }, []);

    const startListening = useCallback(() => {
        if (recognitionInstance && !isListening) {
            setTranscript("");
            recognitionInstance.start();
            setIsListening(true);
        }
    }, [recognitionInstance, isListening]);

    const stopListening = useCallback(() => {
        if (recognitionInstance && isListening) {
            recognitionInstance.stop();
            setIsListening(false);
        }
    }, [recognitionInstance, isListening]);

    return {
        isListening,
        transcript,
        startListening,
        stopListening,
        isSupported,
    };
}
