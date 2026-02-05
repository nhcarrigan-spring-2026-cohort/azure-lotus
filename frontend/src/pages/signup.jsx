import {useAuthContext} from "../context/AuthContext.jsx"

export default function signup() {

    const {login} = useAuthContext()

    const handleRegister = async (e) => {
        e.preventDefault()
        console.log("register")
    }

    const handleLogin = async (e) => {
        e.preventDefault()
        console.log("login")
        await login.mutateAsync({username: "emilys", password: "emilyspass"})
    }

    return (
        <>
            <h1>Signup</h1>
            <button onClick={handleRegister}>Register</button>

            <button
                onClick={handleLogin}
                disabled={login.isPending}
            >Login</button>
        </>
    )
}