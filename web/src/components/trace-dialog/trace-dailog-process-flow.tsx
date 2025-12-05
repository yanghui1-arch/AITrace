import type { Trace, Track } from "@/pages/projects/track/trace-columns";
import {
  Background,
  ReactFlow,
  type Node,
  type Edge,
  MarkerType,
  Panel,
} from "@xyflow/react";
import { TraceProcessNode } from "./trace-process-node";
import dagre from "dagre";
import { useState } from "react";
import { Button } from "../ui/button";
import { Label } from "../ui/label";
import { LLMJsonCard } from "../llm-json-card";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "../ui/sheet";
import { FunctionIOCard } from "../fn-io-card";
import { TraceIONode } from "./trace-process-io-node";
import { NodeSearch } from "../xyflow-ui/node-search";

interface TraceDialogProcessPanelProps {
  input?: Record<string, unknown> | undefined;
  data: Trace;
  output?: Record<string, unknown> | string | undefined;
  errorInfo?: string;
}

const nodeTypes = {
  processNode: TraceProcessNode,
  ioNode: TraceIONode,
};

const findFirstRootTrackStepId = (idx: number, tracks: Track[]): string => {
  if (idx < 0 || idx >= tracks.length) {
    console.warn(
      `pass idx is greater than track length: ${tracks.length} or less than 0. Pass idx: ${idx}`
    );
    return `<ERROR_IDX>${idx}`;
  }
  const newTrack = tracks.slice(idx);
  const rootTrack: Track[] = newTrack.filter(
    (t) => t.step.parent_step_id === null
  );
  return rootTrack[0].step.id;
};

const findLastRootTrackStepId = (tracks: Track[]): string => {
  const reversedTracks = [...tracks].reverse();
  return reversedTracks.filter((t) => t.step.parent_step_id === null)[0].step
    .id;
};

export function TraceDialogProcessPanel({
  input,
  data,
  output,
  errorInfo,
}: TraceDialogProcessPanelProps) {
  const tracks = data.tracks;

  const nodeWidth = 100;
  const nodeHeight = 40;
  const ioWidth = 200;
  // 400 because ScrollArea in FunctionIOCard component obeys max-h-58
  const ioHeight = 400;
  const offsetHeight = 100;

  /* use dagre to calculate the position of nodes */
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setGraph({
    rankdir: "TB",
    nodesep: nodeWidth * 0.3,
    ranksep: nodeHeight * 1.2,
  });
  dagreGraph.setDefaultEdgeLabel(() => ({}));

  if (input) {
    dagreGraph.setNode("input", {
      width: ioWidth,
      height: ioHeight,
    });
  }

  // (parent_id, self_step_id)
  // if step is root node. Don't do anything
  const childGroups = new Map<string, string[]>();
  tracks.forEach((t) => {
    dagreGraph.setNode(`process-${t.step.id}`, {
      width: nodeWidth,
      height: nodeHeight,
    });
    const parentStepId = t.step.parent_step_id;
    if (!parentStepId) return;
    if (!childGroups.get(parentStepId)) {
      childGroups.set(parentStepId, []);
    }
    childGroups.get(parentStepId)!.push(`process-${t.step.id}`);
  });

  if (output) {
    dagreGraph.setNode("output", {
      width: ioWidth,
      height: ioHeight,
    });
  }

  const startProcessNodeStepId = findFirstRootTrackStepId(0, tracks);
  if (input) {
    dagreGraph.setEdge("input", `process-${startProcessNodeStepId}`);
  }
  tracks.forEach((t, index) => {
    const parentStepId = t.step.parent_step_id;
    if (parentStepId) {
      dagreGraph.setEdge(`process-${parentStepId}`, `process-${t.step.id}`);
    } else {
      const nextProcessNodeStepId = findFirstRootTrackStepId(index + 1, tracks);
      dagreGraph.setEdge(
        `process-${t.step.id}`,
        `process-${nextProcessNodeStepId}`
      );
    }
  });

  const lastProcessNodeStepId = findLastRootTrackStepId(tracks);
  if (output) {
    dagreGraph.setEdge(`process-${lastProcessNodeStepId}`, "output");
  }

  dagre.layout(dagreGraph);

  /* xyflow nodes
   * 0 -> input node
   * 1 -> track start node
   * ...
   * tracks.length -> last track node
   * tracks.length + 1 -> output node
   */
  let inputNode: Node | undefined = undefined;
  let outputNode: Node | undefined = undefined;
  if (input) {
    const { x, y } = dagreGraph.node("input");
    inputNode = {
      id: "input",
      data: {
        label: "input",
        input: input,
        total: tracks.length,
      },
      position: {
        x: x,
        y: y - offsetHeight,
      },
      type: "ioNode",
    };
  }
  const processNode: Node[] = tracks.map((track, index) => {
    const { x, y } = dagreGraph.node(`process-${track.step.id}`);
    return {
      id: `process-${track.step.id}`,
      data: {
        label: track.step.name,
        title: track.step.name,
        total: tracks.length,
        hasPrev: index !== 0 || input,
        hasNext: index !== tracks.length - 1 || output,
        llm_inputs: track.step.input.llm_inputs,
        llm_outputs: track.step.output.llm_outputs,
        fn_inputs: track.step.input.func_inputs,
        fn_output: track.step.output.func_output,
        errorInfo: track.step.errorInfo,
      },
      position: {
        x: x,
        y: y,
      },
      type: "processNode",
    };
  });
  if (output) {
    const { x, y } = dagreGraph.node("output");
    outputNode = {
      id: "output",
      data: {
        label: "output",
        output: output,
        errorInfo: errorInfo,
      },
      position: {
        x: x,
        y: y - offsetHeight,
      },
      type: "ioNode",
    };
  }
  const initailProcessNodes: Node[] = [
    ...(inputNode ? [inputNode] : []),
    ...processNode,
    ...(outputNode ? [outputNode] : []),
  ];

  /* xyflow edges
   * (0 -> 1): input -> track start node
   * ....
   * (tracks.length - 1 -> tracks.length): last second -> last
   * (tracks.length -> tracks.length + 1): last track node -> output node
   */
  let inputEdge: Edge | undefined = undefined;
  let outputEdge: Edge | undefined = undefined;
  if (input) {
    inputEdge = {
      id: `edge-0`,
      source: "input",
      target: `process-${startProcessNodeStepId}`,
      type: "default",
      markerEnd: {
        type: MarkerType.Arrow,
      },
    };
  }

  const processEdges: Edge[] = tracks.map((t, index) => {
    if (t.step.parent_step_id) {
      return {
        id: `edge-${index + 1}`,
        source: `process-${t.step.parent_step_id}`,
        target: `process-${t.step.id}`,
      };
    }
    const nextProcessNodeStepId = findFirstRootTrackStepId(index + 1, tracks);
    return {
      id: `edge-${index + 1}`,
      source: `process-${t.step.id}`,
      target: `process-${nextProcessNodeStepId}`,
      type: "default",
      markerEnd: {
        type: MarkerType.Arrow,
      },
    };
  });

  if (output) {
    outputEdge = {
      id: `edge-${tracks.length + 1}`,
      source: `process-${lastProcessNodeStepId}`,
      target: "output",
      type: "default",
      markerEnd: {
        type: MarkerType.Arrow,
      },
    };
  }
  const initialProcessEdges: Edge[] = [
    ...(inputEdge ? [inputEdge] : []),
    ...processEdges,
    ...(outputEdge ? [outputEdge] : []),
  ];

  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [nodeDetailDisplayType, setNodeDetailDisplayType] = useState<
    "llm" | "fn"
  >("llm");

  return (
    <div className="w-full h-[80vh]">
      <ReactFlow
        proOptions={{ hideAttribution: true }}
        defaultNodes={initailProcessNodes}
        defaultEdges={initialProcessEdges}
        nodeTypes={nodeTypes}
        onNodeClick={(_, node) => setSelectedNode(node)}
      >
        <Background />
        <Panel
          className="flex gap-1 rounded-md bg-primary-foreground p-1 text-foreground"
          position="top-left"
        >
          <NodeSearch />
        </Panel>
      </ReactFlow>
      <Sheet open={!!selectedNode} onOpenChange={() => setSelectedNode(null)}>
        {selectedNode &&
          selectedNode.id !== "0" &&
          selectedNode.id !== `${tracks.length + 1}` && (
            <SheetContent className="p-4 max-w-[40vw] md:max-w-[480px] max-h-[calc(100vh-2rem)] overflow-auto">
              <SheetHeader>
                <SheetTitle>
                  {(selectedNode.data.title ?? "Step") as string}
                </SheetTitle>
              </SheetHeader>
              <div className="flex gap-2">
                <Button
                  variant="link"
                  className={
                    nodeDetailDisplayType === "llm"
                      ? "bg-foreground text-black"
                      : ""
                  }
                  onClick={() => {
                    setNodeDetailDisplayType("llm");
                  }}
                >
                  <Label>LLM Input/Output</Label>
                </Button>
                <Button
                  variant="link"
                  className={
                    nodeDetailDisplayType === "fn"
                      ? "bg-foreground text-black"
                      : ""
                  }
                  onClick={() => {
                    setNodeDetailDisplayType("fn");
                  }}
                >
                  <Label>Step Function Input/Output</Label>
                </Button>
              </div>
              {nodeDetailDisplayType === "llm" &&
                (selectedNode.data.llm_inputs ||
                selectedNode.data.llm_outputs ? (
                  <div className="flex flex-col gap-4">
                    <LLMJsonCard
                      jsonObject={
                        selectedNode.data.llm_inputs as Record<string, unknown>
                      }
                      labelTitle="Input"
                    />
                    <LLMJsonCard
                      jsonObject={
                        selectedNode.data.llm_outputs as Record<string, unknown>
                      }
                      labelTitle="Output"
                    />
                  </div>
                ) : (
                  `No llm function is tracked in \`${selectedNode.data.title}\`.`
                ))}
              {nodeDetailDisplayType === "fn" &&
                (selectedNode.data.fn_inputs || selectedNode.data.fn_output ? (
                  <div className="flex flex-col gap-4">
                    <FunctionIOCard
                      data={
                        selectedNode.data.fn_inputs as
                          | Record<string, unknown>
                          | undefined
                      }
                      labelTitle="Input"
                    />
                    <FunctionIOCard
                      data={
                        selectedNode.data.fn_output as
                          | string
                          | Record<string, unknown>
                          | undefined
                      }
                      labelTitle="Output"
                      errorInfo={
                        selectedNode.data.errorInfo as string | undefined
                      }
                    />
                  </div>
                ) : (
                  `No function is tracked in \`${selectedNode.data.title}\`.`
                ))}
            </SheetContent>
          )}
      </Sheet>
    </div>
  );
}
