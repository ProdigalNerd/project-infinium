import { auth, signOut } from "@/auth";
import { prisma } from "@/prisma";
 
export function SignOut() {
  return (
    <form
      action={async () => {
        "use server"
        const session = await auth();        
        await Promise.all([
            prisma.session.deleteMany(
                {
                    where: {
                        userId: {
                            equals: session?.user?.id,
                        },
                    },
                }
            ),
            signOut(),
        ]);
      }}
    >
      <button type="submit">Sign Out</button>
    </form>
  )
}