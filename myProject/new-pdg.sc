/* pdg.sc

   This script returns a complete PDG for functions matching a regex, or the whole CPG if no regex is specified. The PDG
   is represented as two lists, one for the edges and another for the vertices.

   The first list contains all of the edges in the PDG. The first entry in each tuple contains the ID of the incoming
   vertex. The second entry in the tuple contains the ID of the outgoing vertex.

   The second list contains all the vertices in the PDG. The first entry in each tuple contains the ID of the vertex
   and the second entry contains the code stored in the vertex.
*/

import gremlin.scala.{Edge, GremlinScala}

import io.shiftleft.codepropertygraph.generated.EdgeTypes

import scala.collection.mutable

import java.io.PrintWriter  
import java.io.File  
import scala.reflect.io.Directory 
import scala.collection.mutable.Set 

type EdgeEntry = (AnyRef, AnyRef)
type VertexEntry = (AnyRef, String)
type Pdg = (Option[String], List[EdgeEntry], List[VertexEntry])


private def pdgFromEdges(edges: GremlinScala[Edge], filename: String): (List[EdgeEntry], List[VertexEntry]) = {
  val filteredEdges = edges.filter(edge => edge.hasLabel(EdgeTypes.REACHING_DEF, EdgeTypes.CDG)).dedup.l
  //val filteredEdges = edges.dedup.l

  val (edgeResult, vertexResult) =
    filteredEdges.foldLeft((mutable.Set.empty[EdgeEntry], mutable.Set.empty[VertexEntry])) {
      case ((edgeList, vertexList), edge) =>
        val edgeEntry = (edge.inVertex().property("LINE_NUMBER").orElse(""), edge.outVertex().property("LINE_NUMBER").orElse(""))
		//val edgeEntry = (edge.inVertex().id, edge.outVertex().id)
        val inVertexEntry = (edge.inVertex().id, edge.inVertex().property("LINE_NUMBER").orElse(""))
		//val inVertexEntry = (edge.inVertex().id, edge.inVertex().property("CODE").orElse(""))
        val outVertexEntry = (edge.outVertex().id, edge.outVertex().property("LINE_NUMBER").orElse(""))
		//val outVertexEntry = (edge.outVertex().id, edge.outVertex().property("CODE").orElse(""))

        (edgeList += edgeEntry, vertexList ++= Set(inVertexEntry, outVertexEntry))
    }
   
  edgeResult.toList |> "F:\\data\\self_vul_repo\\temp\\hang\\"+filename
  (edgeResult.toList, vertexResult.toList)
}

def subdirs2(dir: File): Array[File] = {
		//val d = dir.listFiles.filter(_.isDirectory)
		val f = dir.listFiles//.filter(_.isFile).toIterator
		//f ++ d.toIterator.flatMap(subdirs2 _)
		
		return f
	}

@main def main(): Unit = {
	val it = subdirs2(new File("F:\\data\\self_vul_repo\\temp"))
	for(d <- it){
		val fileName = d.getName()
		val methodName = d.getName().split("\\$",0)(2).dropRight(2)
		println(methodName)
		cpg.method(methodName).l.map{method =>
        val (edgeEntries, vertexEntries) = pdgFromEdges(method.asScala.out().flatMap(_.asScala.outE()), fileName)
		}
	}
	println("OK..")
}
