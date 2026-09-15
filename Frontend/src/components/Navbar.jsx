import { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { Menu, X, HeartHandshake } from "lucide-react";
export default function Navbar() {
  const [open, setOpen] = useState(false);
  const links = ["About", "Programs", "Projects", "Events", "Volunteer"];
  return (
    <header className="nav">
      <Link className="brand" to="/">
        <span>
          <HeartHandshake />
        </span>
        <div>
          AFAQ<small>FOUNDATION</small>
        </div>
      </Link>
      <nav className={open ? "links open" : "links"}>
        {links.map((x) => (
          <NavLink
            key={x}
            onClick={() => setOpen(false)}
            to={"/" + x.toLowerCase()}
          >
            {x}
          </NavLink>
        ))}
        <Link className="text-link" to="/login">
          Sign in
        </Link>
        <Link className="btn small" to="/donate">
          Donate now
        </Link>
      </nav>
      <button className="menu" onClick={() => setOpen(!open)}>
        {open ? <X /> : <Menu />}
      </button>
    </header>
  );
}
