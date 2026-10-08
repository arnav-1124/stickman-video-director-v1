export interface Shot {
  id: number;
  image: string;
  start: number;
  end: number;
  zoomStart: number;
  zoomEnd: number;
  cx1: number;
  cy1: number;
  cx2: number;
  cy2: number;
  title: string;
}

export interface CameraTransform {
  zoom: number;
  safeCx: number;
  safeCy: number;
  transformOrigin: string;
  transform: string;
  progress: number;
}
