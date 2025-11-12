import { useState } from "react";
import { Button } from "./ui/button";
import { Label } from "./ui/label";
import type { Trace } from "@/pages/projects/track/trace-columns";
import { TraceDialogIOPanel } from "./trace-dialog-io";
import { TraceDialogProcessPanel } from "./trace-dailog-process";

interface TraceDialogMainProps {
  data: Trace;
}

export function TraceDialogMain({ data }: TraceDialogMainProps) {
  const [displayType, setDisplayType] = useState<"io" | "process">("io");
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
        {displayType === "process" && <TraceDialogProcessPanel data={data}/>}
      </div>
    </div>
  );
}
