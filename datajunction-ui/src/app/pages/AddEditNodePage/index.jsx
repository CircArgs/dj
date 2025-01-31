/**
 * Node add + edit page for transforms, metrics, and dimensions. The creation and edit flow for these
 * node types is largely the same, with minor differences handled server-side. For the `query`
 * field, this page will render a CodeMirror SQL editor with autocompletion and syntax highlighting.
 */
import { ErrorMessage, Field, Form, Formik } from 'formik';

import NamespaceHeader from '../../components/NamespaceHeader';
import { useContext, useEffect, useState } from 'react';
import DJClientContext from '../../providers/djclient';
import 'styles/node-creation.scss';
import AlertIcon from '../../icons/AlertIcon';
import ValidIcon from '../../icons/ValidIcon';
import { useParams } from 'react-router-dom';
import { FullNameField } from './FullNameField';
import { FormikSelect } from './FormikSelect';
import { NodeQueryField } from './NodeQueryField';
import { displayMessageAfterSubmit } from '../../../utils/form';

class Action {
  static Add = new Action('add');
  static Edit = new Action('edit');

  constructor(name) {
    this.name = name;
  }
}

export function AddEditNodePage() {
  const djClient = useContext(DJClientContext).DataJunctionAPI;

  let { nodeType, initialNamespace, name } = useParams();
  const action = name !== undefined ? Action.Edit : Action.Add;

  const [namespaces, setNamespaces] = useState([]);

  const initialValues = {
    name: action === Action.Edit ? name : '',
    namespace: action === Action.Add ? initialNamespace : '',
    display_name: '',
    query: '',
    node_type: '',
    description: '',
    primary_key: '',
    mode: 'draft',
  };

  const validator = values => {
    const errors = {};
    if (!values.name) {
      errors.name = 'Required';
    }
    if (!values.query) {
      errors.query = 'Required';
    }
    return errors;
  };

  const handleSubmit = (values, { setSubmitting, setStatus }) => {
    if (action === Action.Add) {
      setTimeout(() => {
        createNode(values, setStatus);
        setSubmitting(false);
      }, 400);
    } else {
      setTimeout(() => {
        patchNode(values, setStatus);
        setSubmitting(false);
      }, 400);
    }
    window.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
  };

  const pageTitle =
    action === Action.Add ? (
      <h2>
        Create{' '}
        <span className={`node_type__${nodeType} node_type_creation_heading`}>
          {nodeType}
        </span>
      </h2>
    ) : (
      <h2>Edit</h2>
    );

  const staticFieldsInEdit = node => (
    <>
      <div className="NodeNameInput NodeCreationInput">
        <label htmlFor="name">Name</label> {name}
      </div>
      <div className="NodeNameInput NodeCreationInput">
        <label htmlFor="name">Type</label> {node.type}
      </div>
    </>
  );

  const primaryKeyToList = primaryKey => {
    return primaryKey.split(',').map(columnName => columnName.trim());
  };

  const createNode = async (values, setStatus) => {
    const { status, json } = await djClient.createNode(
      nodeType,
      values.name,
      values.display_name,
      values.description,
      values.query,
      values.mode,
      values.namespace,
      values.primary_key ? primaryKeyToList(values.primary_key) : null,
    );
    if (status === 200 || status === 201) {
      setStatus({
        success: (
          <>
            Successfully created {json.type} node{' '}
            <a href={`/nodes/${json.name}`}>{json.name}</a>!
          </>
        ),
      });
    } else {
      setStatus({
        failure: `${json.message}`,
      });
    }
  };

  const patchNode = async (values, setStatus) => {
    const { status, json } = await djClient.patchNode(
      values.name,
      values.display_name,
      values.description,
      values.query,
      values.mode,
      values.primary_key ? primaryKeyToList(values.primary_key) : null,
    );
    if (status === 200 || status === 201) {
      setStatus({
        success: (
          <>
            Successfully updated {json.type} node{' '}
            <a href={`/nodes/${json.name}`}>{json.name}</a>!
          </>
        ),
      });
    } else {
      setStatus({
        failure: `${json.message}`,
      });
    }
  };

  const namespaceInput = (
    <div className="NamespaceInput">
      <ErrorMessage name="namespace" component="span" />
      <label htmlFor="react-select-3-input">Namespace</label>
      <FormikSelect
        selectOptions={namespaces}
        formikFieldName="namespace"
        placeholder="Choose Namespace"
        defaultValue={{
          value: initialNamespace,
          label: initialNamespace,
        }}
      />
    </div>
  );

  const fullNameInput = (
    <div className="FullNameInput NodeCreationInput">
      <ErrorMessage name="name" component="span" />
      <label htmlFor="FullName">Full Name</label>
      <FullNameField type="text" name="name" />
    </div>
  );

  const nodeCanBeEdited = nodeType => {
    return new Set(['transform', 'metric', 'dimension']).has(nodeType);
  };

  const updateFieldsWithNodeData = (data, setFieldValue) => {
    const fields = [
      'display_name',
      'query',
      'type',
      'description',
      'primary_key',
      'mode',
    ];
    fields.forEach(field => {
      if (
        field === 'primary_key' &&
        data[field] !== undefined &&
        Array.isArray(data[field])
      ) {
        data[field] = data[field].join(', ');
      }
      setFieldValue(field, data[field] || '', false);
    });
  };

  const alertMessage = message => {
    return (
      <div className="message alert">
        <AlertIcon />
        {message}
      </div>
    );
  };

  // Get namespaces, only necessary when creating a node
  useEffect(() => {
    if (action === Action.Add) {
      const fetchData = async () => {
        const namespaces = await djClient.namespaces();
        setNamespaces(
          namespaces.map(m => ({
            value: m['namespace'],
            label: m['namespace'],
          })),
        );
      };
      fetchData().catch(console.error);
    }
  }, [action, djClient, djClient.metrics]);

  return (
    <div className="mid">
      <NamespaceHeader namespace="" />
      <div className="card">
        <div className="card-header">
          {pageTitle}
          <center>
            <Formik
              initialValues={initialValues}
              validate={validator}
              onSubmit={handleSubmit}
            >
              {function Render({ isSubmitting, status, setFieldValue }) {
                const [node, setNode] = useState([]);
                const [message, setMessage] = useState('');
                useEffect(() => {
                  const fetchData = async () => {
                    if (action === Action.Edit) {
                      const data = await djClient.node(name);

                      // Check if node exists
                      if (data.message !== undefined) {
                        setNode(null);
                        setMessage(`Node ${name} does not exist!`);
                        return;
                      }

                      // Check if node type can be edited
                      if (!nodeCanBeEdited(data.type)) {
                        setNode(null);
                        setMessage(
                          `Node ${name} is of type ${data.type} and cannot be edited`,
                        );
                        return;
                      }

                      // Update fields with existing data to prepare for edit
                      updateFieldsWithNodeData(data, setFieldValue);
                      setNode(data);
                    }
                  };
                  fetchData().catch(console.error);
                }, [setFieldValue]);
                return (
                  <Form>
                    {displayMessageAfterSubmit(status)}
                    {action === Action.Edit && message ? (
                      alertMessage(message)
                    ) : (
                      <>
                        {action === Action.Add
                          ? namespaceInput
                          : staticFieldsInEdit(node)}
                        <div className="DisplayNameInput NodeCreationInput">
                          <ErrorMessage name="display_name" component="span" />
                          <label htmlFor="displayName">Display Name</label>
                          <Field
                            type="text"
                            name="display_name"
                            id="displayName"
                            placeholder="Human readable display name"
                          />
                        </div>
                        {action === Action.Add ? fullNameInput : ''}
                        <div className="DescriptionInput NodeCreationInput">
                          <ErrorMessage name="description" component="span" />
                          <label htmlFor="Description">Description</label>
                          <Field
                            type="textarea"
                            as="textarea"
                            name="description"
                            id="Description"
                            placeholder="Describe your node"
                          />
                        </div>
                        <div className="QueryInput NodeCreationInput">
                          <ErrorMessage name="query" component="span" />
                          <label htmlFor="Query">Query</label>
                          <NodeQueryField
                            djClient={djClient}
                            value={node.query ? node.query : ''}
                          />
                        </div>
                        <div className="PrimaryKeyInput NodeCreationInput">
                          <ErrorMessage name="primary_key" component="span" />
                          <label htmlFor="primaryKey">Primary Key</label>
                          <Field
                            type="text"
                            name="primary_key"
                            id="primaryKey"
                            placeholder="Comma-separated list of PKs"
                          />
                        </div>
                        <div className="NodeModeInput NodeCreationInput">
                          <ErrorMessage name="mode" component="span" />
                          <label htmlFor="Mode">Mode</label>
                          <Field as="select" name="mode" id="Mode">
                            <option value="draft">Draft</option>
                            <option value="published">Published</option>
                          </Field>
                        </div>
                        <button type="submit" disabled={isSubmitting}>
                          {action === Action.Add ? 'Create' : 'Save'} {nodeType}
                        </button>
                      </>
                    )}
                  </Form>
                );
              }}
            </Formik>
          </center>
        </div>
      </div>
    </div>
  );
}
