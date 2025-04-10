
import { getImgUrl } from './utils';


const EntityName = ({entityname}) => {
    return (
        <div style={{width: '100%'}}>
              <img
                src={getImgUrl(entityname)}
                alt={"Company Logo"}
                style={{height: 'auto', width: '100%', objectFit: 'fill'}}
              />
        </div>
    );
}

export default EntityName