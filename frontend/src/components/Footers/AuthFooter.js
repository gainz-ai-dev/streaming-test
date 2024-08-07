import { NavItem, NavLink, Nav, Container, Row, Col } from "reactstrap";

import Copyright from "./Copyright";

const AuthFooter = () => {
  return (
    <>
      <footer className="py-1">
        <Container>
          <Row className="align-items-center justify-content-xl-between">
            <Col xl="12">
              <Nav className="nav-footer justify-content-center">
                <NavItem className="text-sm">
                  <NavLink href="/about-us">
                    About Us
                  </NavLink>
                </NavItem>
                <NavItem className="text-sm">
                  <NavLink href="/privacy">
                    Privacy Policy
                  </NavLink>
                </NavItem>
                <NavItem className="text-sm">
                  <NavLink href="/terms">
                    Terms & Conditions
                  </NavLink>
                </NavItem>
              </Nav>
            </Col>
          </Row>
          <Row className="align-items-center justify-content-xl-between">
            <Col xl="12">
              <Copyright />
            </Col>
          </Row>
        </Container>
      </footer >
    </>
  );
};

export default AuthFooter;
