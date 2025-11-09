import { DataTable } from "@/components/data-table";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import { Link, useLocation, useParams } from "react-router-dom";
import axios from "axios";
import { stepColumns, type Step } from "./step-columns";
import { Separator } from "@/components/ui/separator";
import { RowPanelContent } from "@/components/data-table/data-table-row-panel";
import { Label } from "@/components/ui/label";
import TokensPanel from "@/components/tokens-panel";

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

  useEffect(() => {
    const api = axios.create({
      baseURL: "/api/v0",
      timeout: 5000,
    });

    api.interceptors.response.use(
      (res) => res.data,
      (err) => {
        console.error(err);
        return Promise.reject(err);
      }
    );

    const loadStepDataOfProject = async () => {
      const steps = await api.get(
        `/step/${encodeURIComponent("aitrace_demo")}`
      );
      setStepData(steps.data);
    };
    loadStepDataOfProject();
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
      <div className="container mx-auto py-2">
        <DataTable data={stepData} columns={stepColumns}>
          <RowPanelContent<Step>>
            {(rowData) => (
              <div className="flex gap-4 flex-col">
                <TokensPanel model={rowData.model} usage={rowData.usage} cost={1}/>
                <Separator />
                <div className="flex gap-2">
                  <div className="flex-1 flex flex-col gap-2">
                    <Label htmlFor="input" className="font-semibold">
                      Input
                    </Label>
                    <pre className="text-sm font-mono whitespace-pre-wrap break-words text-left">
                      <code>{JSON.stringify(rowData.input, null, 2)}</code>
                    </pre>
                  </div>
                  <div className="flex-1 flex flex-col gap-2">
                    <Label htmlFor="output" className="font-semibold">
                      Output
                    </Label>
                    <pre className="text-sm font-mono whitespace-pre-wrap break-words text-left">
                      <code>{JSON.stringify(rowData.output, null, 2)}</code>
                    </pre>
                  </div>
                </div>
                
              </div>
            )}
          </RowPanelContent>
        </DataTable>
      </div>
    </div>
  );
}
