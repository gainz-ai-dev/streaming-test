
const Copyright = (props) => {
    return (
        <div className="copyright text-muted text-sm">
            {/* © {new Date().getFullYear()}{" "} */}
            Powered by <a
                className="font-weight-bold ml-1"
                href="https://digitalhealth.net/"
                rel="noopener noreferrer"
                target="_blank"
            >
                Digital Health
            </a>
        </div>
    );
};

export default Copyright;