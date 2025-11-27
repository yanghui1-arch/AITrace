import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import { Link, useLocation, useParams } from "react-router-dom";
import { stepColumns, type Step } from "./step-columns";
import { Separator } from "@/components/ui/separator";
import { StepTable } from "@/components/step-table";
import { traceColumns, type Trace } from "./trace-columns";
import { TraceTable } from "@/components/trace-table";
import http from "@/api/http";

export default function ProjectDetailPage() {
  const { name } = useParams<{ name: string }>();
  const location = useLocation();
  const projectDescription = location.state.description;

  const [navButtonType, setNavButtonType] = useState<
    "step" | "trace" | "conversation"
  >("step");
  const isNavButtonDisabled = (buttonType: string) => {
    return navButtonType === buttonType;
  };

  const [stepData, setStepData] = useState<Step[]>([]);
  const [traceData, setTraceData] = useState<Trace[]>([]);

  useEffect(() => {
    const loadStepDataOfProject = async () => {
      const steps = await http.get(
        `/step/${encodeURIComponent("aitrace_demo")}`
      );
      setStepData(steps.data);
    };
    const loadTraceDataOfProject = async () => {
      const traces = await http.get(
        `/trace/${encodeURIComponent("aitrace_demo")}`
      );
      setTraceData(traces.data);
    };
    loadStepDataOfProject();
    loadTraceDataOfProject();
  }, []);

  return (
    <div className="flex flex-col gap-2 px-4 lg:px-6">
      <h2 className="text-xl font-semibold">{name}</h2>
      <p className="text-muted-foreground mt-2 truncate">
        {projectDescription}
      </p>
      <div className="mt-4">
        <Link to="/projects" className="underline">
          Back to Projects
        </Link>
      </div>
      <div className="flex gap-4 py-2">
        <Button
          variant="link"
          className={isNavButtonDisabled("step") ? "bg-white text-black" : ""}
          onClick={() => {
            if (isNavButtonDisabled("step")) {
              return;
            }
            setNavButtonType("step");
          }}
        >
          Step
        </Button>
        <Button
          variant="link"
          className={isNavButtonDisabled("trace") ? "bg-white text-black" : ""}
          onClick={() => {
            if (isNavButtonDisabled("trace")) {
              return;
            }
            setNavButtonType("trace");
          }}
        >
          Trace
        </Button>
        <Button
          variant="link"
          className={
            isNavButtonDisabled("conversation") ? "bg-white text-black" : ""
          }
          onClick={() => {
            if (isNavButtonDisabled("conversation")) {
              return;
            }
            setNavButtonType("conversation");
          }}
        >
          Conversation
        </Button>
      </div>
      <Separator />
      {navButtonType === "step" ? (
        <StepTable data={stepData} columns={stepColumns} />
      ) : navButtonType === "trace" ? (
        <div>
          <TraceTable data={traceData} columns={traceColumns} />
        </div>
      ) : (
        "Unknow"
      )}
    </div>
  );
}
