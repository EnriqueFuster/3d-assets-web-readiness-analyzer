/// <reference types="vite/client" />

interface ModelViewerConfiguration {
  meshoptDecoderLocation?: string;
}

interface Window {
  ModelViewerElement?: ModelViewerConfiguration;
}

declare namespace React.JSX {
  interface IntrinsicElements {
    "model-viewer": React.DetailedHTMLProps<
      React.HTMLAttributes<HTMLElement> & {
        src?: string;
        alt?: string;
        "camera-controls"?: boolean;
        "auto-rotate"?: boolean;
        "shadow-intensity"?: string;
        exposure?: string;
      },
      HTMLElement
    >;
  }
}
