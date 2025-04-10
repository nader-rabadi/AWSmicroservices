
import { getImgUrl } from './utils';

  const EventName = ({eventname}) => {
    return (
        <div style={{width: '100%'}}>
              <img
                src={getImgUrl(eventname)}
                alt={"Event Banner"}
                style={{height: 'auto', width: '100%', objectFit: 'fill'}}
              />
        </div>
    );
}

export default EventName