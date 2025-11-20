

import React, { useState, useEffect } from 'react';
import { CameraFeed } from './components/CameraFeed';
import { JsonViewer } from './components/JsonViewer';
import { VideoUploader } from './components/VideoUploader';
import type { ViolenceDetectionData, Camera } from './types';
import { Header } from './components/Header';
import { CameraSetup } from './components/CameraSetup';

const App: React.FC = () => {
  const [isConfigured, setIsConfigured] = useState(false);
  const [cameras, setCameras] = useState<Camera[]>([]);
  const [detectionHistory, setDetectionHistory] = useState<ViolenceDetectionData[]>([]);
  const [cameraProbabilities, setCameraProbabilities] = useState<Record<number, number>>({});
  
  const isConnected = isConfigured && cameras.length > 0;

  useEffect(() => {
    if (!isConnected) {
      return;
    }

    console.log("Connecting to real-time stream at http://127.0.0.1:8000/realtime_stream...");
    const eventSource = new EventSource('http://127.0.0.1:8000/realtime_stream');

    eventSource.onmessage = (event) => {
      try {
        const newData: ViolenceDetectionData = JSON.parse(event.data);
        const newProbs: Record<number, number> = {};
        for (const cam of newData.cameras) {
          newProbs[cam.cameraId] = cam.probability;
        }
        setCameraProbabilities(newProbs);
        setDetectionHistory(prevData => [newData, ...prevData.slice(0, 49)]); // Keep last 50 entries
      } catch (error) {
        console.error('Error parsing JSON from SSE stream:', event.data, error);
      }
    };

    eventSource.onerror = (error) => {
      console.error('EventSource failed:', error);
    };

    return () => {
      console.log("Disconnecting from real-time stream...");
      eventSource.close();
    };
  }, [isConnected]);
  
  const handleSetupConnect = (urls: string[]) => {
    const configuredCameras: Camera[] = urls
      // FIX: Explicitly type the return value of the map callback to help TypeScript's inference
      // for the subsequent filter with a type guard.
      .map((url, i): Camera | null => {
        const trimmedUrl = url.trim();
        if (trimmedUrl === '') {
          return null;
        }
        if (trimmedUrl === '0') {
          return {
            id: i + 1,
            name: `Local Webcam`,
            streamUrl: 'local_webcam',
            isLocal: true,
            status: 'connected' as const,
          };
        }
        return {
          id: i + 1,
          name: `Camera ${i + 1}`,
          streamUrl: trimmedUrl,
          isLocal: false,
          status: 'connected' as const,
        };
      })
      .filter((cam): cam is Camera => cam !== null);

    setCameras(configuredCameras);
    setIsConfigured(true);
  };
  
  const handleGlobalDisconnect = () => {
    setCameras([]);
    setDetectionHistory([]);
    setCameraProbabilities({});
    setIsConfigured(false);
  };

  if (!isConfigured) {
    return <CameraSetup onConnect={handleSetupConnect} />;
  }

  return (
    <div className="min-h-screen bg-gray-900 text-gray-200 font-sans">
      <Header onDisconnect={handleGlobalDisconnect} />
      <main className="p-4 lg:p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content: Camera Feeds */}
          <div className="lg:col-span-2">
            <h2 className="text-2xl font-bold mb-4 text-cyan-400">Live Camera Feeds</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
              {cameras.map((cam) => (
                <CameraFeed 
                  key={cam.id} 
                  camera={cam} 
                  probability={cameraProbabilities[cam.id] ?? 0}
                />
              ))}
            </div>
          </div>

          {/* Sidebar: Data Viewer and Uploader */}
          <div className="flex flex-col gap-6">
            <div>
              <h2 className="text-2xl font-bold mb-4 text-cyan-400">Video Analysis</h2>
              <VideoUploader />
            </div>
            <div>
              <h2 className="text-2xl font-bold mb-4 text-cyan-400">Real-time Event Log</h2>
              <JsonViewer data={detectionHistory} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;