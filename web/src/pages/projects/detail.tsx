import { Link, useParams } from "react-router-dom";

export default function ProjectDetailPage() {
  const { name } = useParams<{ name: string }>();

  return (
    <div className="px-4 lg:px-6">
      <h2 className="text-xl font-semibold">Project: {name}</h2>
      <p className="text-muted-foreground mt-2">
        Detail view for project "{name}".
      </p>
      <div className="mt-4">
        <Link to="/projects" className="underline">
          Back to Projects
        </Link>
      </div>
    </div>
  );
}

