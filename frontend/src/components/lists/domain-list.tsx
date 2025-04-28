import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Domain, DomainDeleteResponse } from "@/types/domain";
import { PlusCircle, Trash2 } from "lucide-react";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { useSelector } from 'react-redux';
import { RootState } from "@/redux/store/store";
import { useAppDispatch } from "@/redux/store/hooks";
import { remove } from "@/redux/store/features/domain/domain";
import { deleteDomains } from "@/services/domain";

export function DomainList() {
  const dispatch = useAppDispatch()
  const domains:Domain[] = useSelector((state: RootState) => state.domains);

  const deleteDomainHandler = async (uuid: string) => { 

    try {
      const response: DomainDeleteResponse = await deleteDomains(uuid)
        // Remove the domain from the Redux store
        dispatch(remove(uuid))
    } catch (error) {
      console.error("Error deleting domain:", error);
    }
  }


  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Authorized Domains</h2>
        <Button>
          <PlusCircle className="mr-2 h-4 w-4" /> Add New Domain
        </Button>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Domain</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Registor On</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {domains.map((domain) => (
            <TableRow key={domain.uuid}>
              <TableCell>{domain.domain}</TableCell>
              <TableCell>
                <span
                  className={`px-2 py-1 rounded-full text-xs ${
                    domain.status === "enabled"
                      ? "bg-green-100 text-green-800"
                      : "bg-yellow-100 text-yellow-800"
                  }`}
                >
                  {domain.status}
                </span>
              </TableCell>
              <TableCell>
                {domain.created_at.replace("T", " ").replaceAll("-", " ")}
              </TableCell>
              <TableCell>
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button
                      variant="outline"
                      size="sm"
                      className="text-red-500 hover:text-red-700"
                    >
                      <Trash2 className="h-4 w-4 mr-1" /> Delete
                    </Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                      <AlertDialogDescription>
                        This action cannot be undone. This will permanently
                        delete the domain and all its data.
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancel</AlertDialogCancel>
                      <AlertDialogAction
                        className="bg-red-500 hover:bg-red-700"
                        onClick={() => deleteDomainHandler(domain.uuid)}
                      >
                        Delete
                      </AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
