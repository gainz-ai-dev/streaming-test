import React, { useState, useEffect, useRef } from "react";
import { useLocation, useParams } from "react-router-dom";
import { Col, Row, Spinner } from 'reactstrap';
// core components
import routes from "../routes";
import Chat from "../pages/Chat";

const ChatLayout = (props) => {
    const mainContent = useRef(null);
    const location = useLocation();
    const params = useParams();
    const [loading, setLoading] = useState(true);
    const session_id = params['*'];

    useEffect(() => {
        document.documentElement.scrollTop = 0;
        document.scrollingElement.scrollTop = 0;
        mainContent.current.scrollTop = 0;
    }, [location]);

    useEffect(() => {
        if (session_id) {
            // Assuming fetching some data or waiting for something to be ready
            setTimeout(() => setLoading(false), 1000); // simulate a loading delay
        } else {
            setLoading(false);
        }
    }, [session_id]);

    return (
        <div className="layout-chat h-100">
            <div className="main-content h-100" ref={mainContent}>
                {loading ? (
                    <Row className="mt-2 h-100 flex-grow-1 d-flex">
                        <Col className="h-100 flex-grow-1 d-flex" xl="12">
                            <div className="flex w-100 h-100 flex-col text-center align-content-center">
                                <Spinner type="border" color="secondary" size="sm">
                                    Loading...
                                </Spinner>
                                <span>
                                    {' '}Loading
                                </span>
                            </div>
                        </Col>
                    </Row>
                ) : (
                    session_id ? <Chat id={session_id} /> : <Chat />
                )}
            </div>
        </div>
    );
};

export default ChatLayout;
