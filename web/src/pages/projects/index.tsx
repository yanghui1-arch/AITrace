import { DataTable } from "@/components/data-table";
import { projectColumns } from "./project-columns";
import { useEffect, useState } from "react";
import { projectApi } from "@/api/project";
import { useDataTable } from "@/hooks/use-datatable";
import { ProjectDataTableToolbar } from "@/components/data-table/data-table-toolbar/project-data-table-toolbar";

type Project = {
  name: string;
  description: string;
  cost: number;
  avgDuration: number;
  lastUpdateTimestamp: string;
};

export default function ProjectsPage() {
  const [project, setProject] = useState<Project[]>([]);
  const getProjects = async () => {
    const response = await projectApi.getAllProjects();
    if (response.data.code == 200) {
      const userProjects = response.data.data;
      const projects: Project[] = userProjects.map((p) => ({
        name: p.projectName,
        description: p.description,
        cost: p.cost,
        avgDuration: p.averageDuration,
        lastUpdateTimestamp: p.lastUpdateTimestamp,
      }));
      setProject(projects);
    } else if (response.data.code == 404) {
      console.warn("No projects found.");
    }
  };
  useEffect(() => {
    getProjects();
  }, []);

  const { table } = useDataTable({ columns: projectColumns, data: project });

  return (
    <div className="px-4 lg:px-6">
      <h2 className="text-xl font-semibold">Projects</h2>
      <p className="text-muted-foreground mt-2">
        Create a new one project to track and improve your agent performance!
      </p>
      <div className="container mx-auto py-5 space-y-4">
        <ProjectDataTableToolbar table={table} onCreateProjectSuccessCallback={getProjects}/>
        <DataTable table={table} isNavigate={true} />
      </div>
    </div>
  );
}
