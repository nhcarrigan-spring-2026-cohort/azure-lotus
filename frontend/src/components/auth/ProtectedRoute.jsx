import { useAuthContext } from "../../context/AuthContext"
import { Navigate, useLocation } from "react-router"

export default function ProtectedRoute({children}) {
    const {isAuthenticated} = useAuthContext()
    const location = useLocation()

    if(!isAuthenticated) {
        return <Navigate to="/login" state={{from: location}} replace/>
    }

    return children
}