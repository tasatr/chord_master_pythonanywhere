import React from "react";

const ResultVideo = ({ video }) => {
  if (!video) {
    return <div>
           </div>;
  }
  console.log('###################REsult video:', video);

  return (
    <div>
      <video width="320" height="240" controls>
        <source src={video} type="video/mp4">
        </source>
        Your browser does not support this video format.

      </video>
    </div>
  );
};

export default ResultVideo;
