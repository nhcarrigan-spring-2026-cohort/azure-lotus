import { Routes, Route } from "react-router"
import Navbar from "./components/Navbar.jsx"
import Home from "./pages/Home.jsx"
import About from "./pages/about.jsx"
import Explained from "./pages/explained.jsx"
import Signup from "./pages/signup.jsx"
import NotFound from "./pages/NotFound.jsx" // feat: adding "not found page" to the Routes by "@j3farsale7"

export default function App() {
  return (
    <>

      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/explained" element={<Explained />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="*" element={<NotFound />} />
      </Routes>

    </>
  )
}
