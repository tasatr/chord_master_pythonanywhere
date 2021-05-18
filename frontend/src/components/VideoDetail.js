import React from "react";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";


class VideoDetail extends React.Component {
  constructor(props) {
    super(props);
    this.handleArtistChange = this.handleArtistChange.bind(this);
    this.handleSongChange = this.handleSongChange.bind(this);
    this.handleAnalyzeVideoButton = this.handleAnalyzeVideoButton.bind(this);

  }

  handleArtistChange(e) {
    console.log('#######HandleArtistChange:', e.target.value)
    this.props.handleArtistChange(e.target.value)
  }

  handleSongChange(e) {
    this.props.handleSongChange(e.target.value)
  }

  handleAnalyzeVideoButton(e) {
    this.props.handleAnalyzeVideoButton(e.target.value)
  }

  render() {
    console.log('#########SELECTED VIDEO:', this.props.selectedVideo)
    const video = this.props.selectedVideo;
    if (!video) {
      return <div>
      </div>;
    }

    const videoSrc = `https://www.youtube.com/embed/${video.id.videoId}`;
    console.log(typeof video);

    return (
      <div>
        <div className="ui embed">
          <iframe src={videoSrc} allowFullScreen title="Video player" />
        </div>
        <div className="ui segment">
          <h4 className="ui header">{video.snippet.title}</h4>
        </div>
        <TextField required id="artist" label="Artist" value={this.props.artist} onChange={this.handleArtistChange}/>
        <TextField required id="song" label="Song" value={this.props.song} onChange={this.handleSongChange}/>
        <Button variant="contained" color="primary" onClick={this.handleAnalyzeVideoButton}>
          Analyze this video
        </Button>

      </div>
    )
  }
}
export default VideoDetail
