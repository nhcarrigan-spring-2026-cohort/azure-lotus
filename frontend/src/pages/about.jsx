import useTitle from "../components/customHooks/useTitle"

export default function about() {
    useTitle("About");
    return (
        <>
            <h1>About</h1>
        </>
    )
}