import { memo } from "react";
import {
  BaseNode,
  BaseNodeHeader,
  BaseNodeHeaderTitle,
} from "@/components/base-node";
import { Rocket } from "lucide-react";
import { Handle, Position, type NodeProps } from "@xyflow/react";

export const TraceProcessNode = memo(({ id, data }: NodeProps) => {
  const index = Number(id);
  const total = data.total as number;

  return (
    /* first node doesn't contain input handle and the last node doesn't contain output handle */
    <BaseNode className="w-auto max-w-64">
      {index !== 0 && (
        <Handle
          type="target"
          position={Position.Left}
          className="bg-blue-400! hover:bg-blue-500!"
        />
      )}

      <BaseNodeHeader className="justify-center">
        <Rocket className="size-4" />
        <BaseNodeHeaderTitle className="wrap-break-words text-sm truncate">
          {data.title as string}
        </BaseNodeHeaderTitle>
      </BaseNodeHeader>

      {(!total || index !== total - 1) && (
        <Handle
          type="source"
          position={Position.Right}
          className="bg-blue-400! hover:bg-blue-500!"
        />
      )}
    </BaseNode>
  );
});

TraceProcessNode.displayName = "TraceProcessNode";
