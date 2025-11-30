import { type Table } from "@tanstack/react-table";
import { X } from "lucide-react";
import { useForm, type SubmitHandler } from "react-hook-form";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { DataTableViewOptions } from "@/components/data-table/data-table-view-options";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog";
import { Label } from "../ui/label";
import { projectApi } from "@/api/project";

interface DataTableToolbarProps<TData> {
  table: Table<TData>;
  hasCreateProjectComponent: boolean;
}

type Inputs = {
  projectName: string;
  projectDescription: string;
};

export function DataTableToolbar<TData>({
  table,
  hasCreateProjectComponent = false,
}: DataTableToolbarProps<TData>) {
  const isFiltered = table.getState().columnFilters.length > 0;
  const form = useForm<Inputs>();

  const createProjectSubmit: SubmitHandler<Inputs> = async (data) => {
    try {
      console.log("request body" + JSON.stringify(data));
      const response = await projectApi.createNewProject(data);
      const createProjectName = response.data.data;
      console.log(createProjectName);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="flex items-center justify-between">
      <div className="flex flex-1 items-center space-x-2">
        <Input
          placeholder="Filter projects..."
          value={(table.getColumn("name")?.getFilterValue() as string) ?? ""}
          onChange={(event) =>
            table.getColumn("name")?.setFilterValue(event.target.value)
          }
          className="h-8 w-[150px] lg:w-[250px]"
        />
        {isFiltered && (
          <Button
            variant="ghost"
            onClick={() => table.resetColumnFilters()}
            className="h-8 px-2 lg:px-3"
          >
            Reset
            <X />
          </Button>
        )}
      </div>
      <div className="flex items-center gap-2">
        <DataTableViewOptions table={table} />
        {hasCreateProjectComponent && (
          <Dialog>
            <DialogTrigger asChild>
              <Button size="sm">Create Project</Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-md">
              <form onSubmit={form.handleSubmit(createProjectSubmit)}>
                <div className="flex flex-col gap-2">
                  <DialogHeader>
                    <DialogTitle>Create Project</DialogTitle>
                    <DialogDescription>
                      Create a new project for AITrace
                    </DialogDescription>
                  </DialogHeader>
                  <div className="grid gap-4">
                    <div className="grid gap-3">
                      <Label>Project Name</Label>
                      <Input
                        id="name-1"
                        placeholder="New project name"
                        {...form.register("projectName")}
                      />
                    </div>
                    <div className="grid gap-3">
                      <Label>Description</Label>
                      <Input
                        id="username-1"
                        placeholder="Brief description"
                        {...form.register("projectDescription")}
                      />
                    </div>
                  </div>

                  <DialogFooter className="justify-between">
                    <DialogClose asChild>
                      <Button type="button" variant="destructive">
                        Cancel
                      </Button>
                    </DialogClose>
                    <Button type="submit" variant="secondary">
                      Create
                    </Button>
                  </DialogFooter>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        )}
      </div>
    </div>
  );
}
