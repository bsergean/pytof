
#include <string>
#include <list>
#include <iostream>

using namespace std;

class Node
{
public:
	Node(const string& name): mName(name) {}
	~Node();
	void setAttribute(const string& name, const string& value) { mAttributes.push_back( pair<string, string> (name, value) ); }
	void appendChild(Node* node) { mChildren.push_back(node); }
	string serialize(int indent = 0);

private:
	string mName;
	list<Node*> mChildren;
	list< pair<string, string> > mAttributes;
};

Node::~Node()
{
	for (list<Node*>::iterator it = mChildren.begin(); it != mChildren.end(); ++it) {
		delete *it;
	}
}

string Node::serialize(int indent)
{
	const string eol;
#ifdef WIN32
	eol = "\r\n";
#else
	eol = "\n";
#endif

	string res;
	string padding;
	for (int i = 0; i < indent; i++)
		padding += " ";

	res += padding + "<" + mName;
	// Attributes
	for (list< pair<string, string> >::iterator it = mAttributes.begin(); it != mAttributes.end(); ++it) {
		res += " " + it->first + "=\"" + it->second + "\"";
	}

	// Childs
	if (mChildren.size() > 0) {
		res += ">" + eol;
		for (list<Node*>::iterator it = mChildren.begin(); it != mChildren.end(); ++it) {
			// indent level is 2 chars
			res += (*it)->serialize(indent + 2);
		}
		res += padding + "</" + mName + ">" + eol;
	} else {
		res += " />" + eol;
	}
	return res;
}

int main()
{
	Node* root = new Node("Portfolio");

	Node* folder = new Node("Folder");
	folder->setAttribute("name", "root");
	root->appendChild(folder);

	Node* subfolder = new Node("Folder");
	subfolder->setAttribute("name", "Users");
	folder->appendChild(subfolder);

	string res = root->serialize();
	cout << res << endl;

	/*
	 * Output something like that
	 *
	 * <Portfolio>
	 *   <Folder name="root">
	 *     <Folder name="Users" />
	 *   </Folder>
	 * </Portfolio>
	 *
	 */

	delete root;
}
