
import React from 'react';
import type { ViolenceDetectionData } from '../types';

interface JsonViewerProps {
  data: ViolenceDetectionData[];
}

const formatTimestamp = (isoString: string): string => {
  try {
    const date = new Date(isoString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = String(date.getFullYear()).slice(-2);
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${day}-${month}-${year} ${hours}:${minutes}:${seconds}`;
  } catch (e) {
    return isoString;
  }
};

export const JsonViewer: React.FC<JsonViewerProps> = ({ data }) => {
  return (
    <div className="bg-gray-800/50 rounded-lg shadow-inner h-96 overflow-y-auto p-4 border border-gray-700 font-mono text-xs">
      {data.length === 0 && (
        <div className="flex items-center justify-center h-full text-gray-500">
          <p>Waiting for event data...</p>
        </div>
      )}
      {data.map((entry) => (
        <div key={entry.id} className="mb-3 p-2 rounded-md bg-gray-900/60 border-l-4 border-cyan-700">
          <p className="text-gray-400 mb-2">
            <span className="font-semibold text-gray-300">Timestamp:</span> {formatTimestamp(entry.timestamp)}
          </p>
          <div className="grid grid-cols-2 gap-x-4 gap-y-1">
            {entry.cameras.map(cam => {
              const isAlert = cam.probability > 50;
              return (
                <p key={cam.cameraId}>
                  <span className="text-cyan-400">Cam {cam.cameraId}:</span>
                  <span className={`ml-2 font-bold ${isAlert ? 'text-red-500' : 'text-green-400'}`}>
                    {cam.probability}%
                  </span>
                </p>
              )
            })}
          </div>
        </div>
      ))}
    </div>
  );
};
