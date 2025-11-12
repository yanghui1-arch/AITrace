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
import { TraceIONode } from "./trace-process-io-node";

interface TraceDialogProcessPanelProps {
  input?: Record<string, unknown> | undefined;
  data: Trace;
  output?: Record<string, unknown> | string | undefined;
}

const nodeTypes = {
  processNode: TraceProcessNode,
  ioNode: TraceIONode,
};

export function TraceDialogProcessPanel({
  input,
  data,
  output,
}: TraceDialogProcessPanelProps) {
  const tracks = data.tracks;

  const nodeWidth = 100;
  const nodeHeight = 100;
  /* use dagre to calculate the position of nodes */
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setGraph({
    rankdir: "TB",
    nodesep: nodeWidth * 0.3,
    ranksep: nodeHeight * 1.2,
  });
  dagreGraph.setDefaultEdgeLabel(() => ({}));

  if (input) {
    dagreGraph.setNode("0", {
      width: nodeWidth,
      height: nodeHeight,
    });
  }
  tracks.forEach((_, index) => {
    dagreGraph.setNode((index + 1).toString(), {
      width: nodeWidth,
      height: nodeHeight,
    });
  });
  if (output) {
    dagreGraph.setNode((tracks.length + 1).toString(), {
      width: nodeWidth,
      height: nodeHeight,
    });
  }

  if (input) {
    dagreGraph.setEdge("0", "1");
  }
  tracks.slice(0, -1).forEach((_, index) => {
    dagreGraph.setEdge(index.toString(), (index + 1).toString());
  });
  if (output) {
    dagreGraph.setEdge(
      tracks.length.toString(),
      (tracks.length + 1).toString()
    );
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
    const { x, y } = dagreGraph.node("0");
    inputNode = {
      id: "0",
      data: {
        input: input,
        total: tracks.length,
      },
      position: {
        x: x,
        y: y - nodeHeight,
      },
      type: "ioNode",
    };
  }
  const processNode: Node[] = tracks.map((track, index) => {
    const { x, y } = dagreGraph.node((index + 1).toString());
    return {
      id: (index + 1).toString(),
      data: {
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
        y: y - nodeHeight,
      },
      type: "processNode",
    };
  });
  if (output) {
    const { x, y } = dagreGraph.node((tracks.length + 1).toString());
    outputNode = {
      id: (tracks.length + 1).toString(),
      data: {
        output: output,
        total: tracks.length,
      },
      position: {
        x: x,
        y: y - nodeHeight,
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
      id: `e0`,
      source: "0",
      target: "1",
    };
  }

  const processEdges: Edge[] = tracks.slice(0, -1).map((_, index) => {
    return {
      id: `e${index + 1}`,
      source: (index + 1).toString(),
      target: (index + 2).toString(),
    };
  });

  if (output) {
    outputEdge = {
      id: `e${tracks.length}`,
      source: `${tracks.length}`,
      target: `${tracks.length + 1}`,
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
