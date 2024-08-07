import React from "react";
import { useLocation, Route, Routes, Navigate } from "react-router-dom";
// core components
import Header from "components/Headers/Header";
import Copyright from "components/Footers/Copyright";
import routes from "routes.js";

const MainLayout = (props) => {
    const mainContent = React.useRef(null);
    const location = useLocation();

    React.useEffect(() => {
        document.documentElement.scrollTop = 0;
        document.scrollingElement.scrollTop = 0;
        mainContent.current.scrollTop = 0;
    }, [location]);

    const getRoutes = (routes) => {
        console.log(routes);
        return routes.map((prop, key) => {

            if (prop.layout === "/main") {
                return (
                    <Route path={prop.path} element={prop.component} key={key} exact />
                );
            } else {
                return null;
            }
        });
    };

    return (
        <div className="layout-main pb-5">
            <Header />
            <div className="main-content h-100 pt-3" ref={mainContent}>
                <Routes>
                    {getRoutes(routes)}
                    <Route path="*" element={<Navigate to="/auth/login" replace />} />
                </Routes>
            </div>
            <div className="fixed-bottom py-2 text-center bg-white">
                <Copyright />
            </div>
        </div>
    );
};

export default MainLayout;
