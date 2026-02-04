export default function signup() {

    const handleRegister = async (e) => {
        e.preventDefault()
        console.log("register")
    }

    return (
        <>
            <h1>Signup</h1>
            <button onClick={handleRegister}>Register</button>
        </>
    )
}