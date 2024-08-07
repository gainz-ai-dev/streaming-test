import React from "react";
import { useLocation, Route, Routes, Navigate } from "react-router-dom";
// reactstrap components
import { Container, Row } from "reactstrap";


import routes from "../routes";

const AuthLayout = (props) => {
  const mainContent = React.useRef(null);
  const location = useLocation();

  React.useEffect(() => {
    document.documentElement.scrollTop = 0;
    document.scrollingElement.scrollTop = 0;
    mainContent.current.scrollTop = 0;
  }, [location]);

  const getRoutes = (routes) => {
    return routes.map((prop, key) => {
      if (prop.layout === "/auth") {
        return (
          <Route path={prop.path} element={prop.component} key={key} exact />
        );
      } else {
        return null;
      }
    });
  };

  return (
    <div className="layout-auth">
      <div className="main-content mt-0" ref={mainContent}>
        {/* Page content */}
        <section>
          <div className="page-header min-vh-100">
            <Container>
              <Row>
                <Routes>
                  {getRoutes(routes)}
                  <Route path="*" element={<Navigate to="/auth/login" replace />} />
                </Routes>
              </Row>
            </Container>
          </div>
        </section>
      </div>
    </div>
  );
};

export default AuthLayout;
