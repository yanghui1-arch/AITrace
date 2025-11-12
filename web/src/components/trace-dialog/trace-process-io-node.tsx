import { memo } from "react";
import {
  BaseNode,
  BaseNodeHeader,
  BaseNodeHeaderTitle,
} from "@/components/xyflow-ui/base-node";
import { Rocket } from "lucide-react";
import { Handle, Position, type NodeProps } from "@xyflow/react";

export const TraceIONode = memo(({ data }: NodeProps) => {
  const io = data.input ? data.input : data.output;
  const source = data.input ? true : false;

  return (
    /* first node doesn't contain input handle and the last node doesn't contain output handle */
    <BaseNode className="w-auto max-w-64">
      {!source && <Handle
        type="target"
        position={Position.Top}
        className="bg-blue-400! hover:bg-blue-500!"
      />}

      <BaseNodeHeader className="justify-center">
        <Rocket className="size-4" />
        <BaseNodeHeaderTitle className="wrap-break-words text-sm truncate">
          {JSON.stringify(io)}
        </BaseNodeHeaderTitle>
      </BaseNodeHeader>

      {source && <Handle
        type="source"
        position={Position.Bottom}
        className="bg-blue-400! hover:bg-blue-500!"
      />}
    </BaseNode>
  );
});

TraceIONode.displayName = "TraceIONode";
