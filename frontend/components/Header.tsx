import React from 'react';
import { VideoCameraIcon, PowerIcon } from './icons';

interface HeaderProps {
    onDisconnect: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onDisconnect }) => {
  return (
    <header className="bg-gray-900/80 backdrop-blur-sm shadow-lg p-4 border-b border-gray-700 sticky top-0 z-10">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
            <VideoCameraIcon className="w-8 h-8 text-cyan-400" />
            <h1 className="text-2xl font-bold text-white ml-3">
              ATI VioDetect
            </h1>
        </div>
        <button
          onClick={onDisconnect}
          title="Disconnect all cameras"
          className="flex items-center gap-2 px-3 py-2 bg-gray-700 text-gray-300 rounded-md hover:bg-red-600 hover:text-white transition-colors"
        >
          <PowerIcon className="w-5 h-5" />
          <span className="hidden sm:inline">Disconnect All</span>
        </button>
      </div>
    </header>
  );
};