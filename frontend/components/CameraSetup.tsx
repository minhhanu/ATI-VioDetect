import React, { useState } from 'react';
import { VideoCameraIcon, ArrowRightIcon } from './icons';

interface CameraSetupProps {
  onConnect: (urls: string[]) => void;
}

export const CameraSetup: React.FC<CameraSetupProps> = ({ onConnect }) => {
  const [urls, setUrls] = useState<string[]>(Array(8).fill(''));
  const [error, setError] = useState<string | null>(null);

  const handleUrlChange = (index: number, value: string) => {
    const newUrls = [...urls];
    newUrls[index] = value;
    setUrls(newUrls);
  };

  const handleSubmit = () => {
    // Basic validation: check for at least one non-empty URL
    if (urls.every(url => url.trim() === '')) {
      setError('Please enter at least one camera stream URL.');
      return;
    }
    setError(null);
    onConnect(urls.map(url => url.trim()));
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4 font-sans">
      <div className="w-full max-w-2xl bg-gray-800 rounded-lg shadow-xl p-6 lg:p-8 border border-gray-700">
        <div className="text-center mb-6">
          <VideoCameraIcon className="w-12 h-12 mx-auto text-cyan-400" />
          <h1 className="text-3xl font-bold text-white mt-4">Camera Stream Setup</h1>
          <p className="text-gray-400 mt-2">Enter the MJPEG stream URLs for your cameras to begin monitoring.</p>
        </div>
        
        {error && (
            <div className="mb-4 p-3 bg-red-900/50 text-red-300 border border-red-700 rounded-md text-sm">
                {error}
            </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {urls.map((url, index) => (
            <div key={index}>
              <label htmlFor={`camera-url-${index}`} className="block text-sm font-medium text-gray-300 mb-1">
                Camera {index + 1} URL
              </label>
              <input
                id={`camera-url-${index}`}
                type="text"
                value={url}
                onChange={(e) => handleUrlChange(index, e.target.value)}
                placeholder="e.g., http://192.168.1.100:8080/stream"
                className="w-full bg-gray-900 border border-gray-600 rounded-md px-3 py-2 text-gray-200 focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition"
                aria-label={`Camera ${index + 1} URL`}
              />
            </div>
          ))}
        </div>
        
        <div className="mt-8">
          <button
            onClick={handleSubmit}
            className="w-full flex items-center justify-center gap-2 bg-cyan-600 text-white font-bold py-3 px-4 rounded-md hover:bg-cyan-700 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-cyan-500"
          >
            Start Surveillance
            <ArrowRightIcon className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};
