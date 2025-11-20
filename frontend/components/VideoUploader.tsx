import React, { useState, useRef, useEffect } from 'react';
import type { VideoAnalysisResult } from '../types';
import { UploadIcon, LoadingSpinner, CheckCircleIcon, XCircleIcon } from './icons';

const parseTimeToSeconds = (time: string): number => {
  const parts = time.split(':').map(Number);
  if (parts.length !== 3) {
    console.warn(`Invalid time format: ${time}`);
    return 0;
  }
  const [hours, minutes, seconds] = parts;
  return hours * 3600 + minutes * 60 + seconds;
};


export const VideoUploader: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [videoSrc, setVideoSrc] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<VideoAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      setSelectedFile(file);
      
      if (videoSrc) {
        URL.revokeObjectURL(videoSrc);
      }
      setVideoSrc(URL.createObjectURL(file));

      setUploadResult(null);
      setError(null);
    }
  };

  useEffect(() => {
    // Cleanup function to revoke the object URL when the component unmounts or the source changes
    return () => {
      if (videoSrc) {
        URL.revokeObjectURL(videoSrc);
      }
    };
  }, [videoSrc]);

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    setError(null);
    setUploadResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:8000/upload_video', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server error: ${response.status} - ${errorText || response.statusText}`);
      }
      
      const resultData: VideoAnalysisResult = await response.json();
      
      setUploadResult(resultData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred.');
    } finally {
      setIsUploading(false);
    }
  };
  
  const clearSelection = () => {
    setSelectedFile(null);
    setUploadResult(null);
    setError(null);
    if (videoSrc) {
      URL.revokeObjectURL(videoSrc);
      setVideoSrc(null);
    }
  }

  const getProbabilityColor = (prob: number) => {
    if (prob > 60) return 'text-red-400';
    if (prob > 30) return 'text-yellow-400';
    return 'text-green-400';
  };

  const handleTimestampClick = (time: string) => {
    if (videoRef.current) {
      videoRef.current.currentTime = parseTimeToSeconds(time);
      videoRef.current.play();
    }
  };

  return (
    <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
      <div className="flex flex-col items-center justify-center p-4 border-2 border-dashed border-gray-600 rounded-lg">
        <input
          type="file"
          id="video-upload"
          className="hidden"
          accept="video/*"
          onChange={handleFileChange}
          disabled={isUploading}
        />
        <label htmlFor="video-upload" className={`cursor-pointer ${isUploading ? 'opacity-50' : ''}`}>
          <div className="text-center">
            <UploadIcon className="mx-auto h-12 w-12 text-gray-400" />
            <p className="mt-2 text-sm text-gray-300">
              {selectedFile ? 'Change video' : 'Select a video to upload'}
            </p>
          </div>
        </label>
      </div>

      {selectedFile && (
        <div className="mt-4 text-center">
          <p className="text-sm text-gray-400 truncate">
            Selected: <span className="font-medium text-cyan-400">{selectedFile.name}</span>
          </p>
          <div className="flex justify-center gap-2 mt-2">
            <button
              onClick={handleUpload}
              disabled={isUploading}
              className="flex items-center justify-center px-4 py-2 bg-cyan-600 text-white font-semibold rounded-md hover:bg-cyan-700 disabled:bg-gray-500 transition-colors"
            >
              {isUploading ? (
                <>
                  <LoadingSpinner className="w-5 h-5 mr-2" />
                  Analyzing...
                </>
              ) : (
                'Analyze Video'
              )}
            </button>
            <button onClick={clearSelection} disabled={isUploading} className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 disabled:opacity-50">
              Clear
            </button>
          </div>
        </div>
      )}

      {error && (
        <div className="mt-4 p-3 bg-red-900/50 text-red-300 border border-red-700 rounded-md flex items-center gap-2">
          <XCircleIcon className="w-5 h-5" />
          <p className="text-sm">{error}</p>
        </div>
      )}

      {uploadResult && videoSrc && (
        <div className="mt-4 p-3 bg-gray-900/50 border border-gray-700 rounded-md">
            <h4 className="font-bold text-white flex items-center gap-2 mb-3">
                <CheckCircleIcon className="w-5 h-5 text-green-400" />
                Analysis Complete
            </h4>

            <div className="mb-4 rounded-lg overflow-hidden border-2 border-gray-700">
              <video
                ref={videoRef}
                src={videoSrc}
                controls
                className="w-full aspect-video bg-black"
              />
            </div>

            <div className="mb-3 p-2 bg-gray-800 rounded-md">
                <p className="text-sm">
                    <span className="font-semibold text-gray-300">Overall Violence Probability:</span>
                    <span className={`ml-2 font-bold text-lg ${getProbabilityColor(uploadResult.overallProbability)}`}>
                        {uploadResult.overallProbability.toFixed(1)}%
                    </span>
                </p>
            </div>

            <h5 className="font-semibold text-gray-300 text-sm mb-2">Detailed Timeline (Click to seek):</h5>
            <div className="max-h-48 overflow-y-auto space-y-1 pr-2">
                {uploadResult.timestamps.map((event) => {
                    const isAlert = event.probability > 50;
                    return (
                        <button 
                          key={event.time} 
                          onClick={() => handleTimestampClick(event.time)}
                          className={`w-full flex justify-between items-center text-xs p-1.5 rounded-md text-left transition-colors ${isAlert ? 'bg-red-900/40 hover:bg-red-900/60' : 'bg-gray-800/60 hover:bg-gray-800'}`}
                          title={`Seek to ${event.time}`}
                        >
                            <span className="font-mono text-gray-400">
                                Time: <span className="text-cyan-400">{event.time}</span>
                            </span>
                            <span className={`font-bold ${isAlert ? 'text-red-400' : 'text-gray-300'}`}>
                                {event.probability.toFixed(1)}%
                            </span>
                        </button>
                    );
                })}
            </div>
        </div>
      )}
    </div>
  );
};