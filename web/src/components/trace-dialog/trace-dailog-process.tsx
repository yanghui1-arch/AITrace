import type { Trace } from "@/pages/projects/track/trace-columns";
import { Background, ReactFlow, type Node, type Edge } from "@xyflow/react";
import { TraceProcessNode } from "./trace-process-node";
import dagre from "dagre";
import { useState } from "react";
import { Button } from "../ui/button";
import { Label } from "../ui/label";
import { LLMJsonCard } from "../llm-json-card";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "../ui/sheet";
import { FunctionIOCard } from "../fn-io-card";

interface TraceDialogProcessPanelProps {
  data: Trace;
}

const nodeTypes = {
  processNode: TraceProcessNode,
};

export function TraceDialogProcessPanel({
  data,
}: TraceDialogProcessPanelProps) {
  const tracks = data.tracks;

  const nodeWidth = 100;
  const nodeHeight = 100;
  /* use dagre to calculate the position of nodes */
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setGraph({
    rankdir: "LR",
    nodesep: nodeWidth * 0.3,
    ranksep: nodeHeight * 1.2,
  });
  dagreGraph.setDefaultEdgeLabel(() => ({}));

  tracks.forEach((_, index) => {
    dagreGraph.setNode(index.toString(), {
      width: nodeWidth,
      height: nodeHeight,
    });
  });
  tracks.slice(0, -1).forEach((_, index) => {
    dagreGraph.setEdge(index.toString(), (index + 1).toString());
  });

  dagre.layout(dagreGraph);

  /* xyflow nodes */
  const initailProcessNodes: Node[] = tracks.map((track, index) => {
    const { x, y } = dagreGraph.node(index.toString());
    return {
      id: index.toString(),
      data: {
        title: track.step.name,
        total: tracks.length,
        llm_inputs: track.step.input.llm_inputs,
        llm_outputs: track.step.output.llm_outputs,
        fn_inputs: track.step.input.func_inputs,
        fn_output: track.step.output.func_output,
        errorInfo: track.step.errorInfo,
      },
      position: {
        x: x - nodeWidth / 2,
        y: y,
      },
      type: "processNode",
    };
  });

  /* xyflow edges */
  const initialProcessEdges: Edge[] = tracks.slice(0, -1).map((_, index) => {
    return {
      id: `e${index}`,
      source: index.toString(),
      target: (index + 1).toString(),
    };
  });

  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [nodeDetailDisplayType, setNodeDetailDisplayType] = useState<
    "llm" | "fn"
  >("llm");

  return (
    <div className="w-full h-[45vh]">
      <ReactFlow
        proOptions={{ hideAttribution: true }}
        defaultNodes={initailProcessNodes}
        defaultEdges={initialProcessEdges}
        nodeTypes={nodeTypes}
        onNodeClick={(_, node) => setSelectedNode(node)}
      >
        <Background />
      </ReactFlow>
      <Sheet open={!!selectedNode} onOpenChange={() => setSelectedNode(null)}>
        {selectedNode && (
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
              (selectedNode.data.llm_inputs || selectedNode.data.llm_outputs ? (
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
