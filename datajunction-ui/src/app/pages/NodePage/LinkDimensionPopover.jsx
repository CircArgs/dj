import { useContext, useEffect, useRef, useState } from 'react';
import * as React from 'react';
import DJClientContext from '../../providers/djclient';
import { Form, Formik } from 'formik';
import { FormikSelect } from '../AddEditNodePage/FormikSelect';
import EditIcon from '../../icons/EditIcon';
import { displayMessageAfterSubmit } from '../../../utils/form';

export default function LinkDimensionPopover({
  column,
  node,
  options,
  onSubmit,
}) {
  const djClient = useContext(DJClientContext).DataJunctionAPI;
  const [popoverAnchor, setPopoverAnchor] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const handleClickOutside = event => {
      if (ref.current && !ref.current.contains(event.target)) {
        setPopoverAnchor(false);
      }
    };
    document.addEventListener('click', handleClickOutside, true);
    return () => {
      document.removeEventListener('click', handleClickOutside, true);
    };
  }, [setPopoverAnchor]);

  const columnDimension = column.dimension;

  const handleSubmit = async (
    { node, column, dimension },
    { setSubmitting, setStatus },
  ) => {
    setSubmitting(false);
    console.log('dimension', dimension, 'columnDimension', columnDimension);
    if (columnDimension?.name && dimension === 'Remove') {
      await unlinkDimension(node, column, columnDimension?.name, setStatus);
    } else {
      await linkDimension(node, column, dimension, setStatus);
    }
    onSubmit();
  };

  const linkDimension = async (node, column, dimension, setStatus) => {
    const response = await djClient.linkDimension(node, column, dimension);
    if (response.status === 200 || response.status === 201) {
      setStatus({ success: 'Saved!' });
    } else {
      setStatus({
        failure: `${response.json.message}`,
      });
    }
  };

  const unlinkDimension = async (node, column, currentDimension, setStatus) => {
    const response = await djClient.unlinkDimension(
      node,
      column,
      currentDimension,
    );
    if (response.status === 200 || response.status === 201) {
      setStatus({ success: 'Removed dimension link!' });
    } else {
      setStatus({
        failure: `${response.json.message}`,
      });
    }
  };

  return (
    <>
      <button
        className="edit_button"
        aria-label="LinkDimension"
        tabIndex="0"
        onClick={() => {
          setPopoverAnchor(!popoverAnchor);
        }}
      >
        <EditIcon />
      </button>
      <div
        className="popover"
        role="dialog"
        aria-label="client-code"
        style={{ display: popoverAnchor === false ? 'none' : 'block' }}
        ref={ref}
      >
        <Formik
          initialValues={{
            column: column.name,
            node: node.name,
            dimension: '',
            currentDimension: column.dimension?.name,
          }}
          onSubmit={handleSubmit}
        >
          {function Render({ isSubmitting, status, setFieldValue }) {
            return (
              <Form>
                {displayMessageAfterSubmit(status)}
                <span data-testid="link-dimension">
                  <FormikSelect
                    selectOptions={[
                      { value: 'Remove', label: '[Remove Dimension]' },
                    ].concat(options)}
                    formikFieldName="dimension"
                    placeholder="Select dimension to link"
                    className=""
                    defaultValue={
                      column.dimension
                        ? {
                            value: column.dimension.name,
                            label: column.dimension.name,
                          }
                        : ''
                    }
                  />
                </span>
                <input
                  hidden={true}
                  name="column"
                  value={column.name}
                  readOnly={true}
                />
                <input
                  hidden={true}
                  name="node"
                  value={node.name}
                  readOnly={true}
                />
                <button
                  className="add_node"
                  type="submit"
                  aria-label="SaveLinkDimension"
                  aria-hidden="false"
                >
                  Save
                </button>
              </Form>
            );
          }}
        </Formik>
      </div>
    </>
  );
}
