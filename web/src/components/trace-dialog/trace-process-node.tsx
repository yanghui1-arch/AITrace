import { memo } from "react";
import {
  BaseNode,
  BaseNodeHeader,
  BaseNodeHeaderTitle,
} from "@/components/xyflow-ui/base-node";
import { Rocket } from "lucide-react";
import { Handle, Position, type NodeProps } from "@xyflow/react";

export const TraceProcessNode = memo(({ data }: NodeProps) => {
  const hasPrev = data.hasPrev as boolean;
  const hasNext= data.hasNext as boolean;

  return (
    /* first node doesn't contain input handle and the last node doesn't contain output handle */
    <BaseNode className="w-[100px] h-[100px]">
      {hasPrev && (
        <Handle
          type="target"
          position={Position.Top}
          className="bg-blue-400! hover:bg-blue-500!"
        />
      )}

      <BaseNodeHeader className="justify-center">
        <Rocket className="size-4" />
        <BaseNodeHeaderTitle className="wrap-break-words text-sm truncate">
          {data.title as string}
        </BaseNodeHeaderTitle>
      </BaseNodeHeader>

      {hasNext && (
        <Handle
          type="source"
          position={Position.Bottom}
          className="bg-blue-400! hover:bg-blue-500!"
        />
      )}
    </BaseNode>
  );
});

TraceProcessNode.displayName = "TraceProcessNode";
