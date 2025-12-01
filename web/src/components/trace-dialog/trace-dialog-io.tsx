import type { Trace } from "@/pages/projects/track/trace-columns";
import { LLMJsonCard } from "../llm-json-card";
import { FunctionIOCard } from "../fn-io-card";

interface TraceDialogIOPanelProps {
  data: Trace;
}

export function TraceDialogIOPanel({ data }: TraceDialogIOPanelProps) {
  return (
    <div className="flex flex-col gap-4">
      <TraceDialogInputPanel input={data.input} />
      <TraceDialogOutputPanel
        output={data.output?.func_output}
        errorInfo={data.errorInfo}
      />
    </div>
  );
}

interface TraceDialogInputProps {
  input?: Record<string, unknown>;
}

function TraceDialogInputPanel({ input }: TraceDialogInputProps) {
  return <LLMJsonCard labelTitle="Input" jsonObject={input} />;
}

interface TraceDialogOutputProps {
  output?: Record<string, unknown> | string;
  errorInfo?: string;
}

function TraceDialogOutputPanel({ output, errorInfo }: TraceDialogOutputProps) {
  return (
    <FunctionIOCard labelTitle="Output" data={output} errorInfo={errorInfo} />
  );
}
