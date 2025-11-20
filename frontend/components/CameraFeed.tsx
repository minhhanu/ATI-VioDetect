
import React, { useState, useEffect, useRef } from 'react';
import type { Camera } from '../types';
import { CameraIcon, LoadingSpinner } from './icons';

interface CameraFeedProps {
  camera: Camera;
  probability: number;
}

export const CameraFeed: React.FC<CameraFeedProps> = ({ camera, probability }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);
  const [errorMessage, setErrorMessage] = useState('Stream Unavailable');

  const isAlert = probability > 50;

  useEffect(() => {
    // Reset state whenever the camera source changes
    setIsLoading(true);
    setHasError(false);

    if (!camera.isLocal) {
      // For MJPEG streams, loading/error is handled by the <img> tag's onLoad/onError events
      return;
    }

    // Logic for webcam connection
    let stream: MediaStream | null = null;
    const videoElement = videoRef.current;

    const startWebcam = async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoElement) {
          videoElement.srcObject = stream;
        } else {
          throw new Error("Video element not found.");
        }
      } catch (err) {
        console.error("Error accessing webcam:", err);
        setHasError(true);
        if (err instanceof Error) {
          if (err.name === 'NotAllowedError') {
            setErrorMessage('Permission denied');
          } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
            setErrorMessage('Webcam not found');
          } else {
            setErrorMessage('Could not access webcam');
          }
        } else {
          setErrorMessage('An unknown error occurred');
        }
        setIsLoading(false);
      }
    };

    startWebcam();

    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
      if (videoElement) {
        videoElement.srcObject = null;
      }
    };
  }, [camera.id, camera.isLocal, camera.streamUrl]);

  const alertClasses = "border-red-500 border-2 shadow-lg shadow-red-500/40";
  const normalClasses = "border-gray-700 border-2 hover:border-cyan-500 hover:shadow-cyan-500/20";

  return (
    <div className={`bg-gray-800 rounded-lg shadow-lg overflow-hidden transition-all duration-300 ${isAlert ? alertClasses : normalClasses}`}>
      <div className="p-3 bg-gray-900/50 flex justify-between items-center">
        <h3 className="font-bold text-white truncate flex items-center gap-2">
          <CameraIcon className={`w-5 h-5 ${isAlert ? 'text-red-400' : 'text-cyan-400'}`} />
          {camera.name}
        </h3>
      </div>
      <div className="aspect-video bg-black flex items-center justify-center relative">
        {/* Video/Image elements are always present but hidden until loaded */}
        {camera.isLocal ? (
          <video
            ref={videoRef}
            className={`w-full h-full object-cover ${isLoading || hasError ? 'invisible' : ''}`}
            autoPlay
            playsInline
            muted
            onCanPlay={() => setIsLoading(false)}
            onError={() => {
              setHasError(true);
              setErrorMessage('Video playback error');
              setIsLoading(false);
            }}
          />
        ) : (
          <img
            src={camera.streamUrl}
            alt={`Live feed from ${camera.name}`}
            className={`w-full h-full object-cover ${isLoading || hasError ? 'invisible' : ''}`}
            onLoad={() => setIsLoading(false)}
            onError={() => {
              setHasError(true);
              setErrorMessage('Stream Unavailable');
              setIsLoading(false);
            }}
          />
        )}
        
        {isLoading && (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-400">
            <LoadingSpinner className="w-8 h-8" />
            <p className="mt-2 text-sm">Connecting...</p>
          </div>
        )}

        {hasError && (
           <div className="absolute inset-0 flex flex-col items-center justify-center text-red-400 p-4 text-center">
            <CameraIcon className="w-8 h-8" />
            <p className="mt-2 text-sm font-semibold">{errorMessage}</p>
          </div>
        )}
        
        {!isLoading && !hasError && (
            <div className={`absolute bottom-2 right-2 px-2 py-1 rounded-md text-sm font-bold text-white ${isAlert ? 'bg-red-600/80' : 'bg-black/50'}`}>
            {probability.toFixed(0)}%
            </div>
        )}
      </div>
    </div>
  );
};
