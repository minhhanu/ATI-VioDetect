export interface Camera {
  id: number;
  name: string;
  streamUrl: string;
  isLocal?: boolean;
  status: 'connected' | 'disconnected' | 'error';
}

export interface CameraProbability {
  cameraId: number;
  probability: number;
}

export interface ViolenceDetectionData {
  id: number;
  timestamp: string;
  cameras: CameraProbability[];
}

export interface TimestampProbability {
  time: string;
  probability: number;
}

export interface VideoAnalysisResult {
  overallProbability: number;
  timestamps: TimestampProbability[];
  message: string;
}
