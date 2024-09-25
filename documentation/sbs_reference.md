General
=======

The purpose of this DTD (Document Type Definition) is to define the legal building blocks of the packages XML document. It defines the packages structure with a list of legal elements and attributes.

Parsers
=======

C++ parsers that can be used are:

-	Qt4 DOM or SAX parser
-	Apache XML Xerces-C++ DOM or SAX parser.
-	libXML2 C SAX parser.

SAX parsers allows to do **incremental** parsing in function of users interactions.

Structure
=========

Legend:

-	**element**
-	attribute
-	*element already defined previously*
-	(\*): none, one or more
-	(+): one or more
-	(?): none or one
-	(|): or (exclusive choices)
-	default value

Root
----

This is the structure of the package roughly shown:

-	**package**

	-	identifier: unique string identifier
	-	desc: (?) textual description, optional.
	-	formatVersion: version number of the format of this file
	-	updaterVersion: version number of the last updater applied on this file
	-	featureVersions: an associative table between a string identifying a "feature" and a version string.
		-	**option**: one feature version entry. A given entry must only be present if the feature is used in this package.
				-	name: feature name (string)
				-	value: version (string)
	-	fileUID: unique identifier of this file (for buffering coherence). MS GUID-like format.
	-	versionUID: unique identifier of the current version of this file (different at each file save)

	-	*tree*: a list of metadatas, stored as key/value pairs in a treelist. See tree below. This tree is requiered to only have one level (no sub tree).

	-	**dependencies**: list of external dependencies

		-	**dependency**: one external dependency

			-	filename: name of the file.
			-	uid: unique identifier of this dependency in the package/ context (used as reference).
			-	type: type of dependency (fixed: package).
			-	fileUID: identifier of the file (package/header/fileUID).
			-	versionUID: identifier of the current version of the file (package/header/versionUID). Used for changing repercussion purposes.

	-	**content**: content of the package, tree structure.

		-	...

Content
-------

The *content* is a tree structure of these elements:

### Group

-	**group**: hierarchical group of elements.

	-	identifier: identifier of the group used in the paths that refer to its sub-objects.
	-	uid: unique identifier of this resource in the package/ context.
	-	desc: (?) textual description, optional.
	-	*content*: (?) children of the group.

### Resources

-	**resource**: external files that are not Substance files (images, font, ...)

	-	identifier: identifier of the file.
	-	uid: unique identifier of this resource in the package/ context.
	-	type: (string) type of the resource ("bitmap", "svg", "font", "scene", or "surface").
	-	format: original format of the resource (e.g. BMP, JPG for bitmap type resources. Can be empty for "custom" resources, i.e. not supported natively by the application).
	-	*cookedFormat*: (?) format of the resource after the cooking stage (e.g. RAW or JPEG for bitmap type resources).
	-	*cookedQuality*: (?) quality of resource after the cooking stage (percentage for a bitmap type with a cookedFormat JPEG).
	-	filepath: path and name of the origin file.
	-	**attributes**: various attributes

		-	category: data category. Slash separated strings (optional).
		-	label: User label (string) (optional).
		-	author: User information (string)(optional).
		-	authorURL: URL of the author (string)(optional).
		-	tags: comma separated strings(optional).
		-	description: description (string)(optional).
		-	usertags: user information useful for the 3D engine using the substance engine (UNICODE string) (e.g. filepath and texture name)(optional).
		-	icon: The icon (QIcon raw buffer encoded in Base64) (string) (optional)
		-	hideInLibrary: Boolean that indicate if the Resource will be displayed in the Library component in Substance Designer.

	-	**source**: (?) embedded or managed source. Three children are exclusives.

		-	**externalcopy**: (|) external file copied in a sub-folder of the application and entirely managed.
			-	filename: name of the managed file.

		-	**binembedded**: (|) content embedded in the package file.
			-	datalength: size of the binary data in bytes.
			-	format: (?) zlibbase64, rawbase64, etc.
			-	strdata: data in base64 ASCII format.

	-	**options**: (?) additional options (deprecated)
	-	**tree**: (?) additional options layouted in hierarchical structure.
		-	**treelist**: (\*) a named group of options
			-	name: (string) the name of the sub-group of options
			-	*tree*: a hierarchy of options under this sub-group^
				-	...
		-	**treestr**: (\*) a named option whose value is a string
			-	name: (string) the name of this option value
			-	value: (string) the value of this option
		-	**treeurl**: (\*) a named option whose value is a string that must be interpreted as an URL
			-	name: (string) the name of this option value
			-	value: (string) the value of this option


-	**resourceScene**: meshes/scene files.

	Same as *resource*, but with the following additional sub-elements:

	- isUdim: (boolean)(optional) flag indicating whether this scene must be managed as a mesh unwrapped on multiple uv-tiles.

	- **sceneMaterialMap**: An associative list that store material-graph affectation for the *resourceScene*.

		- **sceneMaterialMapEntry**: (\*) Description of the affections for a given material of the *resourceScene*
			- sceneMaterialName: (string) the affected material name.
			- **uvSetMaterialMapList**: A list that describe the affectations by uv-set
				- **uvSetMaterialMap**: (\*) The affectations for a given uv-set

					- **entries**: A list that associate a *graph* to one or more uv-tile
						- **uvSetMaterialMapEntry**: (\*) An item that associate a *graph* to one or more uv-tile
							- uvTiles: (string) a formatted string that list the uv-ytiles of this entry. At the moment, might be "all" or the uv-tile coordinate formatted as "{xPos}x{yPos}"
							- **material**: the description of the affected material. It only contains a reference to a *graph* at the moment, but it may be extended in the future.
								- sbsGraphUrl: (string) path of the graph definition.

				- **optionsByGraph**: A map that list *options* for some *graph* edited in the context of the currect *resourceScene* \> *resourceScene*'s material \> uv-set.
						- url: (string) path of the graph definition to which the *options* apply.
						- *tree*: the hierarchical options associated with this *graph* in the current context.


### Graph

The graph is not necessary a leaf of the structure, it can contains children content.

-	**graph**: a compositing graph definition (instanced or not).

	-	identifier: name of the graph (name of the definition and the instance if applicable).
	-	uid: unique identifier in the package/ context.

	-	**attributes**: various attributes
		-	category: data category. Slash separated strings (optional).
		-	label: User label (string) (optional).
		-	author: User information (string)(optional).
		-	tags: comma separated strings(optional).
		-	description: description (string)(optional).
		-	usertags: user information useful for the 3D engine using the substance engine (UNICODE string) (e.g. filepath and texture name)(optional).
		-	physicalSize: (float3) The size of the output textures in the real world

	-	**options**: list of specific options.

		-	**option**: (\*) one option entry.
			-	name: (string) option's name.
			-	value: (string) option's value.

	-	**GUIlayoutComp**: (?) GUI flags and options.
		-	display: (?) display type (graph, stack, etc.).
		-	groi: (?) visualized ROI of the graph.
		-	gzoom: (?) graph zoom.

	-	**paraminputs**: (?) list of parameters and compositing inputs of the graph.

		-	**paraminput**: (+) one input of the graph.

			-	identifier: identifier of this input.
			-	uid: unique identifier in the /graph/ context.

			-	**attributes**: various attributes
				-	category: data category. Slash separated strings (optional).
				-	label: User label (string)(optional).
				-	author: User information (string)(optional).
				-	authorURL: URL of the author (string)(optional).
				-	tags: comma separated strings(optional).
				-	description: description (string)(optional).
				-	usertags: user information useful for the 3D engine using the substance engine (UNICODE string) (e.g. filepath and texture name)(optional).
				-	icon: The icon (QIcon raw buffer encoded in Base64) (string) (optional)
				-	hideInLibrary: Boolean that indicate if the Resource will be displayed in the Library component in Substance Designer

			-	disabled: (?)this input is NOT used Y/N.
			-	isConnectable: (?) (boolean) indicates wether this input can the connected to another node by the mean of a connector pin.
			-	type: type of the input (as defined in **Substance Type Code**)

			-	**defaultValue**: (?) default value, depend on the type.
				-	... (see **paramValue and defaultValue** subsection)

			-	**defaultWidget**: (?) default widget used to visualize the entry.

				-	name: name of the widget used to visualize the entry (slider, angle, color, 2D position, etc.).
				-	*options*: list of specific options of the widget type.
					-	...

			-	group: (?) string that contains a group name. Can uses path with '/' separators.
			-	visibleIf: (?) String boolean expression based on graph inputs values
			-	**usages**: list of output usages

				-	**usage**: (\*)
					-	components: usage hint (diffuse, specular, etc.)
					-	name: Combination of RGBA

	-	primaryInput: (?) The uid of the primary (image) input (paraminputs/uid). Used for sub-graphs.
	-	**graphOutputs**: list of compositing outputs of the graph

		-	**graphoutput**: (\*) one compositing output of the graph

			-	identifier: identifier of this output.
			-	uid: unique identifier in the /graph/ context.

			-	**attributes**: various attributes
				-	category: data category. Slash separated strings (optional).
				-	label: User label (string)(optional).
				-	author: User information (string)(optional).
				-	authorURL: URL of the author (string)(optional).
				-	tags: comma separated strings(optional).
				-	description: description (string)(optional).
				-	usertags: user information useful for the 3D engine using the substance engine (UNICODE string) (e.g. filepath and texture name)(optional).
				-	icon: The icon (QIcon raw buffer encoded in Base64) (string)(optional)
				-	hideInLibrary: Boolean that indicate if the Resource will be displayed in the Library component in Substance Designer

			-	**usages**: list of output usages

				-	**usage**: (\*)
					-	components: usage hint (diffuse, specular, etc.)
					-	name: Combination of RGBA

			-	**channels**: (?) channels defined (RGBA, RGB, Grayscale) (ALGUint32 type of value Pfx::Data::Desc::Type)
			-	disabled: (?) this output is disabled Y/N.
			-	group: (?) string that contains a group name. Can uses path with '/' separators.
			-	visibleIf: (?) String boolean expression based on graph inputs values

	-	**compNodes**: the graph definition.

		-	See subsection **compNodes** below.

	-	**baseParameters**: common authoring parameters.

		-	**parameter**: (\*) one authoring parameter definition.

			-	name: name of the authoring parameter to define.
			-	relativeTo: (?) what is the paramValue relative to: 0 nothing (absolute), 1 parent, 2 input (possible only if the container has a primary input). Used for authoring parameters only (common param).
			-	**paramValue**: dynamic definition of the parameter.
				-	... (see **paramValue and defaultValue** subsection)

	-	**GUIObjects**: (?) GUI specific objects.

		-	**GUIObject**: (+) one GUI object entry.

			-	uid: node unique identifier in the /GUIObjects/ context.
			-	GUIName: name of the GUI object
			-	type: type of GUI object (comment, navigation pin, etc.) list to define.
			-	*options*: (?)list of specific options of the GUI object type.
			-	GUIDependency: dependency (format: Type?uid *(?uid...)* the dependency can be multi-uid (not suported))
			-	title: (?) The object Title (string)
			-	frameColor: (?) frame color (RGBA Float)
			-	isTitleVisible: (?) boolean to set title visibility
			-	isFrameVisible: (?) boolean to set frame visibility

			-	**GUILayout**: GUI position/options in the graph frame
				-	gpos: (?) position in the graph layout
				-	docked: (?) object is in a docked state.
				-	dockDistance: (?) original distance between the docked node and its parent (for undock purpose).
				-	size: (?) size of the object.

	-	**root**: (?) Appears when the graph is a root (root graphs outputs are directly computed at runtime, cooking always needed).

		-	disabled: (?) this root is disabled Y/N.
		-	**rootOutputs**: options of the outputs of this root.

			-	**rootOutput**: (\*) one output definition.
				-	output: uid of the graph output (/graph/graphOutputs/graphOutput/uid).
				-	format: (?) texture format of the output.
				-	mipmaps: (?) Depth of the output, 0: full mipmaps pyramid.
				-	usertag: user information useful for the 3Dengine using the substance engine (UNICODE string) (e.g. filepath and texture name).
				-	disabled: (?) output disabled Y/N.
				-	**streamingInfo**: (?) streaming informations (to define).
					-	...

		-	**sbspresets**: (?) list of presets for this graph.

		-	**sbspreset**: (*) Definition of a preset for the tweak values of this graph.

			- label: (string) name (and identifier) of this preset.
			- *usertags*: (?) (string) user-defined formatted metadata associated to this preset.
			- **presetinputs**: list of tweak values
				- **presetinput**: (*) a saved tweak value description
					- uid: tweak uid
					- identifier: tweak identifier
					- type: tweak type (as defined in **Substance Type Code**)
					- **paramValue**: tweak value. (see **paramValue and defaultValue** subsection)


### Function

Non-compositing return type function definition, instanced by instance node.

-	**function**: a function definition.

	-	identifier: name of the function definition.
	-	uid: unique identifier in the package/ context.

	-	**attributes**: various attributes
		-	category: data category. Slash separated strings (optional).
		-	label: User label (string) (optional).
		-	author: User information (string)(optional).
		-	tags: comma separated strings(optional).
		-	description: description (string)(optional).
		-	usertags: user information useful for the 3D engine using the substance engine (UNICODE string) (e.g. filepath and texture name)(optional).
	-	*paraminputs*: (?) list of parameters inputs of the function (See subsection **Graph** above).
	-	type: type of the function return  (as defined in **Substance Type Code**).
	-	**paramValue**: definition of the function.
		-	... (see **paramValue and defaultValue** subsection)

compNodes
---------

Compositing nodes graph definition, each node can be an instance of filter, input, output, external or link type node:

-	**compNodes**

	-	**compNode**: (\*) compositing node definition.

		-	GUIName: (?) name of the node
		-	uid: node unique identifier in the /compNodes/ context.
		-	disabled: (?) this node is disabled Y/N.
		-	*GUILayout*: GUI position/options (See subsection **Graph** above).
		-	**options**: Options list

			-	**option**: option definition
				-	name: option name (string)
				-	value: option value (string)

		-	**compOutputs**: (?) outputs list

			-	**compOutput**: (+) one output (most nodes have one output, instances can have several outputs).

				-	uid: node output unique identifier in the /compNodes/compOutputs/compComput/ context.
				-	comptype: (?) return type of the output (as defined in **Substance Type Code**).

		-	**connections**: (?) input connections list.

			-	**connection**: (+) one connection entry.

				-	entry: entry identifier, specific to CN type.
				-	connRef: uid of the node (/compNode/uid) connected to this input.
				-	connRefOutput: (?) uid of the node output (/compNode/compOutputs/compOutput/uid) connected to this input. Present only if multiple outputs (sub-graph instances).

		-	**compImplementation**: implementation of the compositing node (exclusive)

			-	**compFilter**: (|) filter type compositing node definition

				-	filter: filter type.
				-	**parameters**: filter parameters list (filters parameters, authoring parameters, resources paths, etc.).

					-	**parameter**: (\*) one parameter definition. (same as in Graph)

						-	name: name of the parameter to define.
						-	relativeTo: (?) what is the paramValue
							relative to: 0 nothing(absolute), 1 parent, 2 input (possible only if the container has a primary input). Used for authoring parameters only (common param).
						-	*paramValue*: constant/dynamic definition of the parameter (see **paramValue and defaultValue** subsection).

				-	**paramsArrays**: (?) parameters arrays, e.g. used for gradient data.

					-	**paramsArray**: (+) one parameters array.

						-	name: name (type) of the array
						-	uid: unique identifier of the array in the /paramsArray/ context.
						-	**paramsArrayCells**: list of cells (representing gradient keys)

							-	**paramsArrayCell**: (\*) one array cell.
								-	uid: unique identifier of the cell in the /paramsArrayCell/ context.
								-	*parameters*: parameters list of the cell.

				-	**paramsGraphs**: (?) parameters set graphs, e.g. used for FX-Map parametrization. Data (parameters are separated from node instances to allows data reuse and inheritance).

					-	**paramsGraph**: (+) one parameters set graph.

						-	name: name (type) of the graph
						-	uid: unique identifier of the graph in the /paramsGraphs/ context.
						-	**GUIlayoutPGraph**: (?) GUI flags and options.
							-	display: (?) display type (graph, etc.).
							-	groi: (?) visualized ROI of the graph.
							-	gzoom: (?) graph zoom.

						-	rootnode: (?) uid of the root node, if it exists (/paramsGraph/paramsGraphNodes/paramsGraphNode/uid)
							-	...

						-	**paramsGraphDatas**: data set of nodes, with inheritance system.

							-	**paramsGraphData**: one data set.
								-	identifier: data identifier.
								-	uid: data unique identifier in the (/paramsGraphDatas/) context.
								-	type: data type (for FX-Maps).
								-	inherit: (?) uid of the inherited data if exists (/paramsGraphData/uid).
								-	*parameters*: (?) parameters definition.

						-	**paramsGraphNodes**: nodes list of the parameters graph.

							-	**paramsGraphNode**: (\*) one node of parameters graph.
								-	GUIName: (?) name of the node
								-	uid: node unique identifier in the (/paramsGraphNodes/) context.
								-	type: node type (for FX-Maps).
								-	disabled: (?) this node is disabled Y/N.
								-	*connections*: (?) input (parameterof type ENTRY\_PARAMETER) connections list. connRef are nodes unique identifier references (/paramsGraphNode/uid).
								-	data: uid of the data associated
									with this node (/paramsGraph/paramsGraphDatas/paramsGraphData/uid).
								-	*GUILayout*: GUI position/options (See subsection **Graph** above).

						-	*GUIObjects*: (?) GUI specific objects (See subsection **Graph** above).

			-	**compInstance**: (|) graph instance node

				-	path: path of the graph definition.
				-	*parameters*: filter parameters list.
				-	**outputBridgings**: List of bridging between outputs of this instance node and the
					graph definition.

					-	**outputBridging**: (\*) one bridging.
						-	uid: uid of the compositing node output (/compNode/compOutputs/compOutput/uid).
						-	identifier: graph definition output identifier (/graph/graphOutputs/graphOutput/identifier).

				-	*GUIlayoutComp*: (?) GUI flags and options instance overload (See subsection **Graph** above).

			-	**compInputBridge**: (|) graph input bridge node
				-	entry: input uid (/graph/paraminputs/paraminput/uid).
				-	*parameters*: input parameters list.

			-	**compOutputBridge**: (|) graph output bridge node
				-	output: output uid (/graph/graphOutputs/graphOutput/uid).
				-	connectionColorType: connection color type (optional) (as defined in **Substance Type Code**).

		-	**inputValues**: a list of custom numerical inputs defined by the user on a per-node basis.

			-	**compInputValues**: (\*) a custom numerical input.
				-	identifier: (string) the unique identifier of this inputValue in the context of (/compNode/inputValues).
				-	type: (int) the type of the input (as defined in **Substance Type Code**)


paramValue and defaultValue
---------------------------

**paramValue** and **defaultValue** are almost the same thing: *defaultValue* defines a constant of some type, while *paramValue* define a constant of some type OR a dynamic value (a function graph).
In the other sections "paramValue" refers to *paramValue*, while "defaultValue" and "constantValue" refers to *defaultValue*.

-	**defaultValue**
	-	**constantValueString**: (|) A constant of type string.
	-	**constantValueBool**: (|) A constant of type boolean.
	-	**constantValueInt32**: (|) A constant of type unsigned integer.
	-	**constantValueInt1**: (|) A constant of type vector of 1 integer.
	-	**constantValueInt2**: (|) A constant of type vector of 2 integers.
	-	**constantValueInt3**: (|) A constant of type vector of 3 integers.
	-	**constantValueInt4**: (|) A constant of type vector of 4 integers.
	-	**constantValueFloat**: (|) A constant of type float.
	-	**constantValueFloat1**: (|) A constant of type vector of 1 float.
	-	**constantValueFloat2**: (|) A constant of type vector of 2 floats.
	-	**constantValueFloat3**: (|) A constant of type vector of 3 floats.
	-	**constantValueFloat4**: (|) A constant of type vector of 4 floats.

-	**paramValue**

	-	**constantValueString**: (|) A constant of type string.
	-	**constantValueBool**: (|) A constant of type boolean.
	-	**constantValueInt32**: (|) A constant of type unsigned integer.
	-	**constantValueInt1**: (|) A constant of type vector of 1 integer.
	-	**constantValueInt2**: (|) A constant of type vector of 2 integers.
	-	**constantValueInt3**: (|) A constant of type vector of 3 integers.
	-	**constantValueInt4**: (|) A constant of type vector of 4 integers.
	-	**constantValueFloat**: (|) A constant of type float.
	-	**constantValueFloat1**: (|) A constant of type vector of 1 float.
	-	**constantValueFloat2**: (|) A constant of type vector of 2 floats.
	-	**constantValueFloat3**: (|) A constant of type vector of 3 floats.
	-	**constantValueFloat4**: (|) A constant of type vector of 4 floats.
	-	**dynamicValue**: (|) scripted definition of the parameter (see below)


dynamicValue
------------

This is the definition of a function graph, for use in a **function** resource or in a **parameter**:

	-	rootnode: (?) uid of the node (/dynamicValue/paramNodes/paramNode/uid) connected to the output (if exists).
	-	**paramNodes**: nodes list.

		-	**paramNode**: (\*) one node definition.

			-	uid: (integer) node unique identifier in the (/paramNodes/) context.
			-	function: (string)node kind (`add`, `get_float1`, `const_int4`, `instance`, ...).
			-	type: (?) return type of the node, if the node can handle multiple (as defined in **Substance Type Code**).
			-	*connections*: (?) input connections list. `connRef` are nodes unique identifier references (/paramNode/uid).
			-	**funcDatas**: (?) additional data list (such as variable name for `get*` nodes, or path for `instance`, etc.)
				-	**funcData**: (\*) one additional data entry.
					-	name: additional data identifier (string).
					-	*constantValue*: additional data value, type depend on the context.
						-	... (see **paramValue and defaultValue** subsection (defaultValue case)

			-	*GUILayout*: GUI position/options (See subsection **Graph** above).

	-	*GUIObjects*: (?) GUI specific objects (See subsection **Graph** above).
	-	*options*: list of specific options.
		- ...


Substance Type Codes
--------------------

This defines the types of data represented by an integer value in the Compositing Graph, Function Graph and Fx-Map Graph.
Please note that in some situations the value is composed by or-ing the values of multiple types.
Depending on the context, these composite types may means "all the listed types" or "any of the listed types".

0: No Type or Invalid Type
1: Color Texture
2: Grayscale Texture
3: Color or Grayscale Texture (1+2, aka. Variant Texture)
4: Boolean
16:  Integer1 (uint)
32:  Integer2 (ivec2)
64:  Integer3 (ivec3)
128: Integer4 (ivec4)
256:  Float1 (float)
512:  Float2 (vec2)
1024: Float3 (vec3)
2048: Float4 (vec4)
4096: Fx-Map Graph Node connection
16384: Unicode String
32768: Package Reference or URL
65536: "no return type" (for Function Graph)
131072: Template1 (For template function nodes)


MDL Integration
---------------

### MDLGraph

The MDL Graph defines a graph for compositing MDL (Material Language Definition) materials. It's the compositing *Graph* counterpart for MDL.

-	**mdl_graph**: MDL graph definition.

	-	identifier: (string) name of the graph.
	-	uid: (unsigned integer) unique identifier in the *package/* context.

	-	**attributes**: various attributes, mainly related to Library management, and that didn't fit in the annotations (see below).
		-	category: (?) (string) a category for this graph.
		-	hideInLibrary: (?) Boolean that indicate if this graph should be hidden if its package is made part of the Library. Default to false.
		-	icon: (?) (string) an icon (QIcon raw buffer encoded in Base64) to be used as thumbs for this graph.

	-	**mdl_annotations**: supplementary attributes defined in a way that match the MDL specification, and that would be exported with the graph as such.
		-	... (see below)

	-	**nodes**: list of (MDL) nodes defining this graph.
		-	**mdl_node**: (\*) definition of one node.
			-	uid: (unsigned integer) unique identifier in the */nodes/* context.
			-	**connections**: (?) input connections list
				-	**connection**: (+) one connection entry
					-	... (see definition of */compNodes/compNode/connections/connection*)
			-	**GUILayout**: GUI position/options (see definition of *graph/GUIObjects/GUIObject/GUILayout*).
			-	**mdl_node_implementation**: implementation of the MDL node (exclusive)

				-	**mdl_node_implementation_constant**: (|) constant node implementation. This kind of node may define the equivalent of a literal constant of a given type, or be used as an input for the *mdl_graph*.
					-	**mdl_operands**: the list of parameter of this node. For constant node in particular, there should be exactly one operand.
						-	... (see below)
					-	is_exposed: (?) (bool) Boolean that indicate if the node is exposed, i.e. if it defines a graph input.
					-	type_modifier: (?) (integer) enum or bitfield that indicate the type modifier(s) (varying, uniform, const, ...) of the constant. Default to no modifier ('auto')
					-	**mdl_annotations**: if this constant is an input (*is_exposed*), defines the MDL annotations associated to this input.
						-	... (see below)

				-	**mdl_node_implementation_mdl_instance**: (|) native function or native material node implementation (any instance of a definition that can be found in the MDL library). These are the most common nodes.
					-	mdl_path: (string) The true MDL path of the definition from which this instance comes, including parameters declaration if any. (e.g. 'mdl::math::cross(float3,float3)')
					-	**mdl_operands**: The possibly empty list of parameter of this node.
						-	... (see below)
					-	**outputBridgings**: (?) a list of output for this node.
						-	**outputBridging**: (\*) one output description.
							-	uid: (unsigned int) unique identifier in the */mdl_node/* context, used for *connection*.
							-	identifier: (string) the identifier of the output

				-	**mdl_node_implementation_selector**: (|) implementation of a special node that allows access to struct members (a kind of operator.()).
					-	struct_type: (string) The struct's MDL path from which we want to extract a member. It should match the type of what is connected to the unique input of this node.
					-	name: (string) The selected member name.
					-	type: (string) The selected member type (its MDL path).

				-	**mdl_node_implementation_mdl_graph_instance**: (|) *MDLGraph* instance node implementation.
					-	path: (string) package's url to the referenced graph, just like */compNodes/compNode/compImplementation/compInstance/path*.
					-	**mdl_operands**: The possibly empty list of parameter of this node, which should be synchronized with the referenced graph's inputs.
						-	... (see below)

				-	**mdl_node_implementation_sbs_instance**: (|) *Graph* instance node implementation
					-	path: (string) package's url to the referenced graph, just like for *mdl_node_implementation_mdl_graph_instance*.
					-	**parameters**: custom parameters used for the integration of Substance *Graph* in MDL.
						-	**parameter**: (\*) one parameter
							-	name: (string) The parameter identifier. Must match the one of the referenced graph, or a predefined name (e.g. '$tiling')
							-	is_default_value: (?)(bool) Boolean that indicate if the value of this parameter is the default one
							-	**value**: value of this parameter. The various type defined below are mutually exclusives.
								-	bool: (|)
								-	int1: (|)
								-	int2: (|)
								-	int3: (|)
								-	int4: (|)
								-	float1: (|)
								-	float2: (|)
								-	float3: (|)
								-	float4: (|)
								-	string: (|)
					-	**sbs_parameters**: parameters holding the values of the *Graph*'s input tweaks. See *graph/paraminputs*.
						-	**parameter**: (\*) see *parameter* just above.
					-	**sbs_common_parameters**: parameters that are common to all Substance *Graph*s. See *graph/baseParameters*.
						-	**parameter**: (\*) see *parameter* just above.
					-	*outputBridgings*: a list of output that reflects the outputs of the referenced *Graph*.
						-	*outputBridging*: (\*) one output description.
							-	uid: (unsigned int) unique identifier in the */mdl_node/* context.
							-	identifier: (string) the matching identifier of the output of the referenced graph.
					-	**input_bridgings**: a list of input that reflects the input textures of the referenced *Graph*.
						-	**input_bridging**: (\*) one input description.
							-	local_identifier: (string) unique identifier in the */mdl_node/* context.
							-	identifier: (string) the matching identifier of the output of the referencced graph.

	-	**gui_objects**: (?) GUI specific objects (comments, frames, pins).
		- 	**GUIObject**: (\*) see definition of *graph/GUIObjects/GUIObject*.
	-	*tree*: a hierarchical structure to store various options relative to this *MDLGraph*
	-	root_node_uid: (unsigned int) uid of the node set as root (output) for this graph. Must be a material instance node.
	-	**inputs**: All the inputs of this graph. For each input, there must exist a matching constant node in the graph.
		-	**mdl_input**: (\*) One input definition
			-	nodeuid: (unsigned int) the uid of the matching constant node in this graph

### MDLOperands

Defines a list of parameters used in some MDL nodes and MDL Annotations

-	**mdl_operands**: MDLOperands definition. For each item, there are three possible implementations:
	-	**mdloperandvalue**: (\*) A simple base-type operand.
		-	name: (string) the name of the operand.
		-	type: (string) the type of the operand (its type's MDL path).
		-	value: (string) the value of the operand, formatted as described in **MDL Value Format** section below.
		-	**mdl_operand_meta_data**: various meta-data on this parameter, that are unrelated to annotations.
			-	accept_connection: (?)(bool) indicate if the operand is can accept connection (the pin is visible and active for this parameter)
			-	is_default_value: (?)(bool) indicate if the value of this operand is the default one.
	-	**mdloperandstruct**: (\*) A compound type (struct) operand.
		-	name: (string) the name of the operand.
		-	type: (string) the struct type of the operand (its MDL path).
		-	**members**: a list of sub-operand, describing the members of the struct
			- ... see *mdl_operands*
		-	**mdl_operand_meta_data**: see just above.
	-	**mdloperandarray**: (\*) An array operand.
		-	name: (string) the name of the operand.
		-	type: (string) the array type of the operand (its MDL path).
		-	**items**: a list of sub-operand, describing the items of the array
			- ... see *mdl_operands*
		-	**mdl_operand_meta_data**: see just above.

### MDLAnnotations

The MDL annotations are defined at multiple levels in the MDL Graph, and gives additional information about what they are attached to. They match the MDL specification, and are exported in the MDL module.

-	**mdl_annotations**: MDLAnnotations definition: a list of annotations.
	-	**mdl_annotation**: (\*)
		-	mdl_path: (string) The MDL path of the annotation, including parameters declaration. (e.g. 'mdl::anno::hard_range(int2,int2)')
		-	**mdl_operands**: The possibly empty list of parameter of this annotation. See *MDLOperands* above.

### MDL Value Format

Here is a description a the way operands' value are serialized in the SBS for MDL:

For numeric and color values (`int`, `float`, `double`, `color`, `intN`, `floatN`, `doubleN`, `floatNxM`, `doubleNxM`, with `N` and `M` being `2`, `3` or `4`),
values are written in decimal, using a point (`.`) as decimal point, and separated by semicolons (`;`). For matrix types, the components are flattened in row-major order.
For example, the matrix of type `float2x3`:
`	[1.1, 4.4]`
`	[2.2, 5.5]`
`	[3.3, 6.6]`
Will be serialized as `1.1;4.4;2.2;5.5;3.3;6.6`.

For booleans (bool, bool2, bool3, bool4), the serialized string is `true` or `false`, separated by semicolons (`;`) for vectors.

For string type, the string is serialized as such.

For complex types that reference a resource (BSDF, VDF, EDF, textures, ...), the dependency url of the matching resource is used (e.g. `pkg:///Resources/my_bsdf_name?dependency=1288424710`)

A special value type is "Call": it represent the value returned by the call to a specific function with specific parameters. This kind of values appears as default values on the parameters of some native MDL nodes.
The serialized string is the runtime reference to the IRay object behind the call, which is its MDL path followed by a unique id. For example, you will often see something like:
`mdl::material(bool,material_surface,material_surface,color,material_volume,material_geometry)_83873438`
for the default material_root.

Structures and Arrays are handle through sub-operands. See *MDLOperands* above.


Visible If Expression
=====================

Use logical operators to check values:

-	`&&`: And
-	`||`: Or
-	`!`: Not
-	`<`, `>`, `<=`, `>=`, `==`, `!=`: Comparison

To read the value of an existing Graph Input:

-	use the map "input" with the identifier as string for the key:

	-	E.G.: `input["MyInput"]`
-	if input's type is Boolean, Integer1, Float1

	-	E.G.:

		-	`input["MyInput"]` if `MyInput` is boolean.
		-	`input["MyInput"] < 1` if `MyInput` is Integer1 or Float1

-	if input's type is IntegerN, FloatN with N ranging from two to four, use
	properties named `.x`, `.y`, `.z`, `.w` to access the field values

	-	E.G.:

		-	`input["MyInput"].z < 1` if `MyInput` is Float3 or
			Float4 or Integer3 or Integer4
		-	`input["MyInput"].w < 1` if `MyInput` is Float4 or
			Integer4

Parenthesis are also available to define priorities.
