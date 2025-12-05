import { memo } from "react";
import { Handle, Position, type NodeProps } from "@xyflow/react";
import { FunctionIOCard } from "../fn-io-card";

export const TraceIONode = memo(({ data }: NodeProps) => {
  const io = (data.input ? data.input : data.output) as string | Record<string, unknown>;
  const source = data.input ? true : false;
  const errorInfo = data.errorInfo as string | undefined;

  return (
    /* first node doesn't contain input handle and the last node doesn't contain output handle */
    <div className="w-[200px]">
      {!source && (
        <Handle
          type="target"
          position={Position.Top}
          className="bg-blue-400! hover:bg-blue-500!"
        />
      )}

      <FunctionIOCard
        data={io}
        labelTitle={source ? "Input" : "Output"}
        errorInfo={errorInfo}
        className="nowheel break-all"
      />

      {source && (
        <Handle
          type="source"
          position={Position.Bottom}
          className="bg-blue-400! hover:bg-blue-500!"
        />
      )}
    </div>
  );
});

TraceIONode.displayName = "TraceIONode";
