function SourceCard({ source, page }) {

    return (

        <div className="source-card">
            <span className="source-card-name">{source}</span>
            <span className="source-card-page">p.{page}</span>
        </div>

    );

}

export default SourceCard;
