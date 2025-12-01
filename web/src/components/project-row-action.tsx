import { useState } from "react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuGroup,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
import { MoreHorizontal, Pencil, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { Project } from "@/pages/projects/project-columns";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { useForm } from "react-hook-form";
import { projectApi } from "@/api/project";
import { toast } from "sonner";

interface ProjectRowActionsProps {
  project: Project;
  onRefresh: () => void;
}

type UpdateParams = {
  projectName: string;
  projectDescription: string;
};

export function ProjectRowActions({ project, onRefresh }: ProjectRowActionsProps) {
  const [openEdit, setOpenEdit] = useState(false);
  const [openDelete, setOpenDelete] = useState(false);
  const form = useForm<UpdateParams>({
    defaultValues: {
      projectName: project.name,
      projectDescription: project.description,
    }
  });

  const editUpdateSubmit = (data: UpdateParams) => {
    console.log(data);
  };

  const deleteProject = async (projectName: string) => {
    const response = await projectApi.deleteProject({projectName});
    setOpenDelete(false);
    if (response.data.code == 200) {
      await onRefresh();
      toast.success(response.data.data);
    }
  }

  return (
    <>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" className="h-8 w-8 p-0">
            <MoreHorizontal className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>

        <DropdownMenuContent className="w-40" align="end">
          <DropdownMenuGroup>
            <DropdownMenuItem onClick={() => setOpenEdit(true)}>
              Edit
              <Pencil className="ml-auto h-4 w-4" />
            </DropdownMenuItem>

            <DropdownMenuSeparator />

            <DropdownMenuItem onClick={() => setOpenDelete(true)}>
              <span className="text-red-400">Delete</span>
              <Trash2 className="ml-auto h-4 w-4" />
            </DropdownMenuItem>
          </DropdownMenuGroup>
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Edit Dialog */}
      <Dialog open={openEdit} onOpenChange={setOpenEdit}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit project: {project.name}</DialogTitle>
          </DialogHeader>
          <form onSubmit={form.handleSubmit(editUpdateSubmit)}>
            <div className="flex flex-col gap-2">
              <div className="grid gap-2">
                <div className="grid gap-2">
                  <Label>Project Name</Label>
                  <Input
                    id="name-1"
                    {...form.register("projectName")}
                  />
                </div>
                <div className="grid gap-2">
                  <Label>Description</Label>
                  <Input
                    id="description-1"
                    {...form.register("projectDescription")}
                  />
                </div>
              </div>
              <DialogFooter>
                <Button onClick={() => setOpenEdit(false)}>Close</Button>
                <Button type="submit" variant="destructive">
                  Update
                </Button>
              </DialogFooter>
            </div>
          </form>
        </DialogContent>
      </Dialog>

      {/* Delete Dialog */}
      <Dialog open={openDelete} onOpenChange={setOpenDelete}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="text-red-500">Confirm Delete</DialogTitle>
            <DialogDescription>
              Delete action can't be reversed. Are you sure to delete?
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="secondary" onClick={() => setOpenDelete(false)}>
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={() => deleteProject(project.name)}
            >
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
