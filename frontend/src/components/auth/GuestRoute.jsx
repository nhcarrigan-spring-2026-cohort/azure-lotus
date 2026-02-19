// Only unauthenticated users can access this route, e.g. login / sign up

import {useAuthContext} from "../../context/AuthContext.jsx";
import {Navigate, useLocation} from "react-router"
import {Link} from "react-router"

export default function GuestRoute({children}) {
    const {isAuthenticated, logout } = useAuthContext()
    const location = useLocation()

    if (isAuthenticated) {
        return (
            <>
                <div>You are already logged in!</div>
                <div>
                    <Link to="/">back</Link>
                    <br/>
                    <Link to="/dashboard">dashboard</Link>
                    <br/>
                    <Link to="/" onClick={logout}>logout</Link>
                </div>
            </>
        )

        // return <Navigate to="/login" state={{from: location}} replace/>
    }

    return children
}