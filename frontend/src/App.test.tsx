import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("./api", () => ({
  ApiError: class ApiError extends Error {},
  analyzeAsset: vi.fn(),
  optimizeAsset: vi.fn(),
}));

vi.mock("./components/ModelViewer", () => ({
  ModelViewer: ({ title }: { title: string }) => <div>{title} viewer</div>,
}));

import App from "./App";
import { analyzeAsset, optimizeAsset } from "./api";
import { assetReport, comparisonReport } from "./test/fixtures";

const analyzeMock = vi.mocked(analyzeAsset);
const optimizeMock = vi.mocked(optimizeAsset);

function glbFile(): File {
  return new File([new Uint8Array([0x67, 0x6c, 0x54, 0x46])], "Box.glb", {
    type: "model/gltf-binary",
  });
}

describe("App", () => {
  beforeEach(() => {
    analyzeMock.mockReset();
    optimizeMock.mockReset();
  });

  it("uploads a GLB, analyzes it, and renders the backend report", async () => {
    analyzeMock.mockResolvedValue(assetReport());
    const user = userEvent.setup();
    render(<App />);

    await user.upload(screen.getByLabelText("GLB file"), glbFile());
    await user.click(screen.getByRole("button", { name: "Analyze asset" }));

    expect(analyzeMock).toHaveBeenCalledWith(expect.any(File), "mobile");
    expect(await screen.findByRole("heading", { name: "Box.glb" })).toBeInTheDocument();
    expect(screen.getByText("Ready for target")).toBeInTheDocument();
  });

  it("shows a useful error when analysis fails", async () => {
    analyzeMock.mockRejectedValue(new Error("The GLB is invalid."));
    const user = userEvent.setup();
    render(<App />);

    await user.upload(screen.getByLabelText("GLB file"), glbFile());
    await user.click(screen.getByRole("button", { name: "Analyze asset" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("The GLB is invalid.");
  });

  it("renders comparison and both viewers after optimization", async () => {
    const comparison = comparisonReport();
    optimizeMock.mockResolvedValue({
      archive: new Blob(["zip"]),
      optimizedAsset: new Blob(["glb"], { type: "model/gltf-binary" }),
      comparison,
    });
    const user = userEvent.setup();
    render(<App />);

    await user.upload(screen.getByLabelText("GLB file"), glbFile());
    await user.click(screen.getByRole("button", { name: "Analyze + optimize" }));

    expect(optimizeMock).toHaveBeenCalledWith(expect.any(File), "mobile");
    expect(await screen.findByRole("heading", { name: "Before / after" })).toBeInTheDocument();
    expect(screen.getByText("Original viewer")).toBeInTheDocument();
    expect(screen.getByText("Optimized viewer")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Download result ZIP" })).toBeEnabled();
  });
});
