import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import { Link, useLocation, useParams } from "react-router-dom";
import { stepColumns, type Step } from "./step-columns";
import { Separator } from "@/components/ui/separator";
import { StepTable } from "@/components/step-table";
import { traceColumns, type Trace } from "./trace-columns";
import { TraceTable } from "@/components/trace-table";
import http from "@/api/http";
import { useDataTable } from "@/hooks/use-datatable";

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

  const refreshStepData = async () => {
    const response = await http.get(
      `/v0/step/${encodeURIComponent(name as string)}`
    );
    setStepData(response.data.data);
  };

  const refreshTraceData = async () => {
    const response = await http.get(
      `/v0/trace/${encodeURIComponent(name as string)}`
    );
    setTraceData(response.data.data);
    await refreshStepData()
  };

  const { table: stepTable } = useDataTable({columns: stepColumns, data: stepData, onRefresh: refreshStepData})
  const { table: traceTable } = useDataTable({ columns: traceColumns, data: traceData, onRefresh: refreshTraceData})

  useEffect(() => {
    const loadStepDataOfProject = async () => {
      const response = await http.get(
        `/v0/step/${encodeURIComponent(name as string)}`
      );
      setStepData(response.data.data);
    };
    const loadTraceDataOfProject = async () => {
      const response = await http.get(
        `/v0/trace/${encodeURIComponent(name as string)}`
      );
      setTraceData(response.data.data);
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
        <StepTable table={stepTable} />
      ) : navButtonType === "trace" ? (
        <div>
          <TraceTable table={traceTable} />
        </div>
      ) : (
        "Unknow"
      )}
    </div>
  );
}
