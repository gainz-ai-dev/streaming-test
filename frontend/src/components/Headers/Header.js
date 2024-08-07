import { Container, Navbar } from "reactstrap";

const Header = () => {
  return (
    <>
      <Navbar className="navbar navbar-expand-lg shadow-none border-bottom py-3">
        <Container className="">
          <a className="h4 font-weight-bolder my-0" href="/">
            Bevan
          </a>
          <button className="navbar-toggler shadow-none ms-2" type="button" data-bs-toggle="collapse" data-bs-target="#navigation" aria-controls="navigation" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon mt-2">
              <span className="navbar-toggler-bar bar1"></span>
              <span className="navbar-toggler-bar bar2"></span>
              <span className="navbar-toggler-bar bar3"></span>
            </span>
          </button>
          <div className="collapse navbar-collapse w-100 pt-3 pb-2 py-lg-0">
            <ul className="navbar-nav navbar-nav-hover mx-auto">
              <li className="nav-item dropdown dropdown-hover mx-2">
                <a href="/about-us" className="nav-link ps-2 d-flex justify-content-between cursor-pointer align-items-center text-dark font-weight-bolder">
                  About Us
                </a>
              </li>
              <li className="nav-item dropdown dropdown-hover mx-2">
                <a href="/privacy" className="nav-link ps-2 d-flex justify-content-between cursor-pointer align-items-center text-dark font-weight-bolder">
                  Privacy Policy
                </a>
              </li>
              <li className="nav-item dropdown dropdown-hover mx-2">
                <a href="/terms" className="nav-link ps-2 d-flex justify-content-between cursor-pointer align-items-center text-dark font-weight-bolder">
                  Terms & Conditions
                </a>
              </li>
            </ul>
            <ul className="navbar-nav d-lg-block d-none">
              <li className="nav-item">
                <a href="/auth/login" className=" btn btn-sm btn-primary mb-0 me-1">Login</a>
              </li>
            </ul>
          </div>
        </Container>
      </Navbar>
    </>
  );
};

export default Header;
