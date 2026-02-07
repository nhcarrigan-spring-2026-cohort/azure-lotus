import './Home.css';
import { Link } from "react-router"

export default function Home() {
  return (
    
      <div className="home">
        <main className="home-main">
          <div className="home-content">
          <p className="home-lead">
            Connecting and Caring for Seniors
          </p>
          <Link className="home-more" to="/about" >Discover More</Link>
          </div>

          <img className="home-img" src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%2Fid%2FOIP.GBZwc50uhRqcDUICs1K7sAHaEg%3Fpid%3DApi&f=1&ipt=d0c234658ea797787b9f41454499d9cc1ad181c91db2abefe0ab55601a5edaad&ipo=images" />
        </main>

        <hr />

      </div>

      

    
  );
}
