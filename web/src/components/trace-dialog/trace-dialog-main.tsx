import { useEffect, useState } from "react";
import { Button } from "../ui/button";
import { Label } from "../ui/label";
import type { Trace } from "@/pages/projects/track/trace-columns";
import { TraceDialogIOPanel } from "./trace-dialog-io";
import { TraceDialogProcessPanel } from "./trace-dailog-process-flow";
import { traceApi, type Track } from "@/api/trace";

interface TraceDialogMainProps {
  data: Trace;
}

export function TraceDialogMain({ data }: TraceDialogMainProps) {
  const [displayType, setDisplayType] = useState<"io" | "process">("io");
  const [tracks, setTracks] = useState<Track[]>([]);

  useEffect(() => {
    const getTracks = async () => {
      const response = await traceApi.getTracks(data.id);
      if (response.data.code === 200) {
        setTracks(response.data.data);
      }
      else setTracks([]);
    }
    getTracks();
  }, [setTracks, data])

  return (
    <div className="flex gap-4 flex-col">
      <div className="flex gap-2">
        <Button
          variant="link"
          className={displayType === "io" ? "bg-foreground text-black" : ""}
          onClick={() => {
            setDisplayType("io");
          }}
        >
          <Label>Input/Output</Label>
        </Button>
        <Button
          variant="link"
          className={
            displayType === "process" ? "bg-foreground text-black" : ""
          }
          onClick={() => {
            setDisplayType("process");
          }}
        >
          <Label>Process Flow</Label>
        </Button>
      </div>
      <div>
        {displayType === "io" && <TraceDialogIOPanel data={data}/>}
        {displayType === "process" && <TraceDialogProcessPanel tracks={tracks} input={data.input} output={data.output?.func_output} errorInfo={data.errorInfo}/>}
      </div>
    </div>
  );
}
